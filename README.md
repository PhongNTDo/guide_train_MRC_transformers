#  GUIDE TRAINING MRC WITH TRANSFORMERS

## 1. Requirement
Install library: transformers
```js
pip install transformers
```
## 2. Data
### 2.1. Model PhoBERT, DistilBERT
Use data with the same format as **train-v2.0.json** and **dev-v2.0.json** (format of data files SQuAD, ViQuAD is released).
### 2.2. Model mBERT, BERT (base & large), XLM-Roberta
Use data with the same format as **train-v2.0-new_format.json** and **dev-v2.0-new_format.json**

Convert the data file from format 2.1 to format 2.2 as follows:
```js
python3 convert_format.py dev-v2.0.json dev-v2.0-new_format.json 2
```
where *dev-v2.0.json* is the data file with format 2.1, *dev-v2.0-new_format.json* is the data file (format 2.2) created after the conversion is complete and the last number is the version of the data (2 is for unanswerable question and answerable question, 1 is for answerable question only)

## 3. Training
### 3.1. Model PhoBERT, DistilBERT
Use code in folder old_ver.

**For PhoBERT:**
```js
python run_squad.py \
  --model_name_or_path vinai/phobert-large \
  --train_file <path-to-training-file> \
  --predict_file <path-to-dev-file> \
  --model_type roberta \
  --do_train \
  --do_eval \
  --per_gpu_train_batch_size 8 \
  --learning_rate 2e-5 \
  --num_train_epochs 2 \
  --max_seq_length 256 \
  --max_answer_length 128 \
  --max_query_length 128 \
  --overwrite_output_dir  \
  --doc_stride 128 \
  --version_2_with_negative \
  --output_dir './PhoBERTlarge_finetuned_ViQuAD/'   #path-to-save-model
```

**For distilBERT:**
Similar to PhoBERT with:
```js
--model_name_or_path distilbert-base-multilingual-cased \
--model_type distilbert \
```

For both PhoBERT and DistilBERT, if the data does not have unanswerable questions, delete the rows --version_2_with_negative
### 3.2. Model mBERT, BERT (base & large) and XLM-Roberta
Use code in folder new_ver.

**For XLM-Roberta**

```js
python run_qa.py \
  --model_name_or_path xlm-roberta-large \
  --train_file <path-to-training-file> \
  --validation_file <path-to-dev-file> \
  --do_train \
  --do_eval \
  --per_device_train_batch_size 4 \
  --learning_rate 2e-5 \
  --num_train_epochs 2 \
  --max_seq_length 384 \
  --max_answer_length 128 \
  --doc_stride 128 \
  --save_steps 1000 \
  --overwrite_output_dir \
  --version_2_with_negative True \
  --output_dir  './XLMR_finetuned_Squad' #path-to-save-model
 ```
 
 **BERT (base & large), mBERT**: similar to XLM-Roberta, just change model_name_or_path accordingly.
 
 If data dose not have unanswerable question: remove line *--version_2_with_negative True* or set *--version_2_with_negative False* 
 
 ## 4. Evaluation
 
 ### 4.1. PhoBERT and DistilBERT
 Use code folder old_ver
 
 PhoBERT
 ```js
 python run_squad.py \
  --model_name_or_path  <path-to-save-model> \
  --predict_file <path-to-test-file \
  --model_type roberta \
  --do_eval \
  --per_gpu_train_batch_size 12 \
  --learning_rate 2e-5 \
  --num_train_epochs 2 \
  --max_seq_length 384 \
  --max_answer_length 128 \
  --max_query_length 128 \
  --overwrite_output_dir  \
  --doc_stride 128 \
  --version_2_with_negative \
  --output_dir <path-to-folder-save-result-and-predictions>
 ```

DistilBERT is similar to PhoBERT

### 4.2. BERT, mBERT, XLM-Roberta

```js
python run_qa.py \
  --model_name_or_path <path-to-save-model> \
  --test_file <path-to-test-file> \
  --do_predict \
  --per_device_train_batch_size 4 \
  --learning_rate 2e-5 \
  --num_train_epochs 2 \
  --max_seq_length 384 \
  --max_answer_length 128 \
  --doc_stride 128 \
  --save_steps 1000 \
  --overwrite_output_dir \
  --version_2_with_negative True \
  --output_dir <path-to-folder-save-result-and-predictions>
 ```
 
 ### 4.3. Evaluate with official script of SQuAD
 
Use for all of model, with data with unanswerable and data without unanswerable
```js
python evaluate.py <file-test-data> <file-predictions>
```

where <file-test-data> is the test data file with format 2.1, <file-predictions> is the predictions file created throught evaluation, file in <path-to-folder-save-result-and-predictions>.

**Note for all of model**: If you want the model trained with data with unanswerable questions to predict answers on all questions, remove line *--version_2_with_negative* when evaluating.
  
  
Written by ***PhongDNT***   
