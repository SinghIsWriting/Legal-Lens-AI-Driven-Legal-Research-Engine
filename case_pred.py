import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence
#from transformers import BertTokenizer
import joblib  # Used for saving and loading the label encoder
import re

# Define the TextClassifier model class (ensure this matches your original model's structure)
class TextClassifier(nn.Module):
    def _init_(self, vocab_size, embed_size, hidden_size, num_layers, num_classes):
        super(TextClassifier, self)._init_()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True, dropout=0.5)
        self.fc = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # Embedding layer
        x = self.embedding(x)
        
        # LSTM layers
        lstm_out, _ = self.lstm(x)
        
        # Taking the last hidden state for classification
        out = lstm_out[:, -1, :]
        
        # Fully connected layer and softmax
        out = self.fc(out)
        out = self.softmax(out)
        
        return out


# Load the saved tokenizer
# Load the tokenizer from the .pkl file
tokenizer = joblib.load('tokenizer.pkl')

# Load the saved label encoder
label_encoder = joblib.load('label_encoder.pkl')

# Load the trained model (Ensure the parameters match those used during training)
model = TextClassifier(
    vocab_size=tokenizer.vocab_size,
    embed_size=128,   # Ensure this matches your training configuration
    hidden_size=256,  # Ensure this matches your training configuration
    num_layers=2,     # Ensure this matches your training configuration
    num_classes=len(label_encoder.classes_)
)

model.load_state_dict(torch.load('best_lstm_model.pth', weights_only=True))

model.eval()

def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    return text


# Function to predict the label of new text
def predict(text):
    
    text = '''
    The case concerns a legally constituted public body of an international carrier, which is deemed to have submitted to the jurisdiction of Indian courts, including under the Code of Civil Procedure (CPC) of 1908.

The CPC allows the Central Government to grant consent for a foreign state to be sued in an Indian court, with certain conditions. Section 86(2) of the CPC provides that consent can be given with respect to a specified suit, several specified suits, or all suits of a specified class or classes.

The Air Act and its rules provide that there is a deemed consent granted by the Central Government for a specified class of suits under the Air Act, as per Section 86(1) of the CPC.

Additionally, the Air Act states that its provisions are in addition to and not in derogation of other laws in force.
'''
    text = preprocess_text(text)

    # Tokenize the input text
    tokenized_text = tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=128)
    input_ids = pad_sequence([torch.tensor(tokenized_text)], batch_first=True)

    # Make prediction
    with torch.no_grad():
        output = model(input_ids)

    # Convert output to predicted label
    predicted_label_idx = torch.argmax(output, dim=1).item()
    prediction = label_encoder.inverse_transform([predicted_label_idx])[0]
    
    #print(prediction)

    res = ''
    if(prediction == 1):
        res = 'The judgment will be favorable to the petitioner (the party initiating the case).'
    elif (prediction == 0):
        res = 'The judgment will be neutral or will not clearly favor either party, possibly involving a direction to follow legal procedures or a dismissal without a decisive outcome.'
    else:
        res = "The judgment will be unfavorable to the petitioner, meaning the opposing party will win or the petitioner's claims will be rejected."
    
    
    print("this is output: ",res)

    return res

# # Example usage
if __name__ == "_main_":
    text = predict(' ')