# Quick start
```
bash run.sh ./data/testing_data.csv result.csv
```

# Model

Put training data into /data/ and train a new model with default parameters:
```
python train.py
```
The model will be stored in /save/. Or, just download a trained model from https://www.dropbox.com/s/d1lfnv6rhc247me/model.ckpt-80000.zip?dl=0 and put all files into /save/.

# Generate a result
```
python sample.py
```
Make sure that testing data exists in /data/ and model files exist in /save/

# Performance
Master model (baseline): 0.39615

setting: One LSTM layer trained 80000 batches with batch size = 50, vocabulary size = 40000, and sequence length = 25. Training loss is about 4.1. Use max sampling while predicting. 

Best model :



# Tuning

Vocabulary size (train.py)

Number of LSTM layers (train.py)

Length of sequences (train.py)

Dropout (train.py)

Consider next words while predicting (sample.py)



# Reuse the codes from

https://github.com/sherjilozair/char-rnn-tensorflow

https://github.com/hunkim/word-rnn-tensorflow
