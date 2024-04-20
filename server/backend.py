#from crypt import methods
from flask import Flask, request, jsonify
import pickle
import cleanpost as cp
from flask_cors import CORS, cross_origin
import numpy as np
import torch
from scipy.special import softmax
app = Flask(__name__)
CORS(app)


with open('model.pkl', 'rb') as handle:
   model = pickle.load(handle)

with open('bert_tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)


def predict(user_input):
    # Tokenize code input
    class_labels = [
    "Tensor Operations",
    "Pre-trained Model",
    "Optimized Learning Algorithms",
    "Data Augmentation",
    "Memory Leaks",
    "Checkpoint",
    "Early Stopping",
    "Quantization",
    "Efficient Read-Write"
]
    user_input_encoding = tokenizer(user_input, truncation=True, padding=True, return_tensors='pt')

# Convert input to torch tensors
    input_ids = user_input_encoding['input_ids']
    attention_mask = user_input_encoding['attention_mask']

# Create a list of class labels
    #class_labels = list(set(train_labels))

# Make prediction
    model.eval()
    with torch.no_grad():
        output = model(input_ids, attention_mask=attention_mask)
        logits = output.logits
        probabilities = torch.softmax(logits, dim=1)
        predicted_label_index = probabilities.argmax(dim=1).item()

# Map predicted label index to class label

    return class_labels[predicted_label_index]



# text -> clean -> title + body -> keywords of title & body -> get pattern
@app.route('/', methods=['POST'])
def index():
    # print("inside post...")
    request_data = request.get_json()
    # print(request_data)
    title = request_data['title']
    body = cp.clean_body(request_data['body'])  # body in HTML format
    body=title+body
    label = predict(body); 
    print(label)
    return jsonify({
        "pattern": label
    })
    

app.run(host='0.0.0.0', port=8500)

