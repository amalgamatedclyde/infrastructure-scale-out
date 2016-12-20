import os
import time
import cPickle
import logging
import numpy as np
import pandas as pd
import caffe
import warnings

# Clyde changed
# REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
# REPO_DIRNAME = os.getcwd()
# REPO_DIRNAME = "/home/clyde/markable/py-features-api"
REPO_DIRNAME = "/home/ubuntu/py-features-api"
UPLOAD_FOLDER = '/tmp/caffe_demos_uploads'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])


class ClassificationError(Exception):
    """raised for classifier errors"""


class ImagenetClassifier(object):

    model_def_file = '{}/models/deploy.prototxt'.format(REPO_DIRNAME)
    pretrained_model_file = '{}/models/bvlc_reference_caffeneplatformt.caffemodel'.format(REPO_DIRNAME)
    mean_file = '{}/python/caffe/imagenet/ilsvrc_2012_mean.npy'.format(REPO_DIRNAME)
    class_labels_file = '{}/data/ilsvrc12/synset_words.txt'.format(REPO_DIRNAME)
    bet_file = '{}/data/ilsvrc12/imagenet.bet.pickle'.format(REPO_DIRNAME)
    gpu_mode= False
    image_dim = 256
    raw_scale  = 255.
    logging.info('Loading net and associated files...')
    caffe.set_mode_cpu()
    net = caffe.Classifier(
        model_def_file, pretrained_model_file,
        image_dims=(image_dim, image_dim), raw_scale=raw_scale,
        mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0)
    )

    with open(class_labels_file) as f:
        labels_df = pd.DataFrame([
                                     {
                                         'synset_id': l.strip().split(' ')[0],
                                         'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                                     }
                                     for l in f.readlines()
                                     ])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        labels = labels_df.sort('synset_id')['name'].values
    bet = cPickle.load(open(bet_file))
    bet['infogain'] -= np.array(bet['preferences']) * 0.1

    def classify_image(self, image):
        try:
            starttime = time.time()
            scores = self.net.predict([image], oversample=True).flatten()
            endtime = time.time()
            indices = (-scores).argsort()[:5]
            predictions = self.labels[indices]
            meta = [
                (p, '%.5f' % scores[i])
                for i, p in zip(indices, predictions)
                ]
            expected_infogain = np.dot(
                self.bet['probmat'], scores[self.bet['idmapping']])
            expected_infogain *= self.bet['infogain']
            infogain_sort = expected_infogain.argsort()[::-1]
            bet_result = [(self.bet['words'][v], '%.5f' % expected_infogain[v])
                          for v in infogain_sort[:5]]

            return (True, meta, bet_result, '%.3f' % (endtime - starttime))

        except Exception as err:  # can throw IOError
            raise ClassificationError('Something went wrong when classifying the '
                                      'image. Maybe try another one?')
            # logging.info('Classification error: %s', err)
            return (False, 'Something went wrong when classifying the '
                           'image. Maybe try another one?')

