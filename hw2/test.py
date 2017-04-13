import tensorflow as tf
import numpy as np
import os
import sys
import time
import argparse
from six.moves import cPickle
from model import Video_Caption_Generator
from utils import data_preprocess, get_video_feat, get_padding_caption
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--train_video_feat_path', type=str, default='MLDS_hw2_data/training_data/feat/',
						help='directory which contains training video feature files')
	parser.add_argument('--test_video_feat_path', type=str, default='MLDS_hw2_data/testing_data/feat/',
						help='directory which contains testing video feature files')
	parser.add_argument('--train_label_json', type=str, default='MLDS_hw2_data/training_label.json',
						help='json file of training captions and corresponding video id')
	parser.add_argument('--test_label_json', type=str, default='MLDS_hw2_data/testing_public_label.json',
						help='json file of testing captions and corresponding video id')
	parser.add_argument('--result_file', type=str, default='output.json',
						help='result file')
	parser.add_argument('--init_from', type=str, default='save',
						help="""initialize from saved model at this path.
						'config.pkl'	: configuration;
						'checkpoint'	: paths to model file(s) (created by tf).
										Note: this file contains absolute paths, be careful when moving files around;
						'model.ckpt-*'	: file(s) with model definition (created by tf)
						""")
	args = parser.parse_args()
	test(args)

def test(args):

	assert os.path.isfile(os.path.join(args.init_from,"config.pkl")), "config.pkl file does not exist in path %s" % args.init_from
	# open old config and check if models are compatible
	with open(os.path.join(args.init_from, 'config.pkl'), 'rb') as f:
		saved_args = cPickle.load(f)

	with open(os.path.join(args.init_from, 'vocab.pkl'), 'rb') as f:
		vocab = cPickle.load(f)

	vocab_inv = {v:k for k, v in vocab.items()}

	print(saved_args)

	_, _, _, _, test_feat_id, test_caption = data_preprocess(args.train_label_json,args.test_label_json)

	print(vocab_inv[359])

	model = Video_Caption_Generator(saved_args,n_vocab=len(vocab),infer=True)
	
	with tf.Session() as sess:

		tf.global_variables_initializer().run()
		print("Initialized")
		
		saver = tf.train.Saver(tf.global_variables())
		ckpt = tf.train.get_checkpoint_state(args.init_from)

		if ckpt and ckpt.model_checkpoint_path: # args.init_from is not None:
			saver.restore(sess, ckpt.model_checkpoint_path)
			print("Model restored %s" % ckpt.model_checkpoint_path)

		result = []

		for i in range(1):#range(len(test_feat_id)):
			this_test_feat_id = test_feat_id[i]

			# get vdieo features
			# notes: the second argument to get_video_feat must be np.array
			current_feat, current_feat_mask = get_video_feat(args.test_video_feat_path, np.array([this_test_feat_id]))

			this_gen_idx, probs = sess.run([model.gen_caption_idx,model.pred_probs],feed_dict={
										model.video: current_feat,
										model.video_mask : current_feat_mask,
										})
			# print(this_gen_idx)
			# argm = np.argmax(probs[0])	
			# print(len(probs))			
			# print(np.argmax(probs[0]))
			# print(vocab_inv[argm])
			this_gen_words = []

			for k in range(len(this_gen_idx)):
				this_gen_words.append(vocab_inv.get(this_gen_idx[k],'<PAD>'))

			this_gen_words = np.array(this_gen_words)

			punctuation = np.argmax(this_gen_words == '<EOS>') + 1
			
			if punctuation > 1:
				this_gen_words = this_gen_words[:punctuation]

			print(this_gen_words)

			this_caption = ' '.join(this_gen_words)
			this_caption = this_caption.replace('<BOS> ', '')
			this_caption = this_caption.replace(' <EOS>', '')

			this_answer = {}
			this_answer['caption'] = this_caption
			this_answer['id'] = this_test_feat_id

			print('Id: %s, caption: %s' % (this_test_feat_id, this_caption))

			result.append(this_answer)

		with open(args.result_file, 'w') as fout:
			json.dump(result, fout)

if __name__ == '__main__':
	main()