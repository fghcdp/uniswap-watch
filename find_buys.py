import pickle

token_matches = pickle.load(open('token_matches.p', 'rb'))
print(token_matches[0])
print(token_matches[0].keys())
print(token_matches[0]['name'])
