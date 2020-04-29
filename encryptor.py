#!/usr/bin/env python3
import sys
import argparse

def statistic(text, alphabet):
    alphabet_size = len(alphabet)
    stats = list()
    summ = 0
    for i in range(alphabet_size):
        stats.append(0)
    for i in range(len(text)):
        if text[i].lower() in alphabet:
            stats[alphabet.index(text[i].lower())] += 1
            summ += 1
    for i in range(alphabet_size):
        stats[i] /= summ
        stats[i] = str(stats[i])
    return stats

def take_out_of_file(given_file):
    with open(given_file, 'r') as text_file:
        text = ''.join([line for line in text_file])
        text_file.close()
    return text

def put_into_file(given_file, text):
    with open(given_file, 'w') as text_file:
        text_file.write(text)
        text_file.close()

def all_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('type')
    parser.add_argument('--cipher')
    parser.add_argument('--key')
    parser.add_argument('--input-file')
    parser.add_argument('--output-file')
    parser.add_argument('--text-file')
    parser.add_argument('--model-file')
    return parser.parse_args(sys.argv[1:])

def caesar(text, alphabet, key):
    alphabet_size = len(alphabet)
    key = key % alphabet_size
    new_text = list()
    for i in range(len(text)):
        if text[i] in alphabet:
            letter_number = alphabet.index(text[i])
            letter_number += key
            if letter_number >= alphabet_size:
                letter_number -= alphabet_size
            new_text.append(alphabet[letter_number])
        else:
            new_text.append(text[i])
    return ''.join(new_text)

def vigenere(text, alphabet, key):
    alphabet_size = len(alphabet)
    new_text = list()
    key = key
    while (len(key) < len(text)):
        key += key
    for i in range(len(text)):
        digit_key = alphabet.index(key[i])
        if text[i] in alphabet:
            letter_number = alphabet.index(text[i])
            letter_number += digit_key
            if letter_number >= alphabet_size:
                letter_number -= alphabet_size
            new_text.append(alphabet[letter_number])
        else:
            new_text.append(text[i])
    return ''.join(new_text)


alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_lower = 'abcdefghijklmnopqrstuvwxyz' 
arguments = all_args()
if arguments.type == 'encode':
    if arguments.cipher == 'caesar':
        if arguments.input_file != None:
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        new_text = caesar(text, alphabet, int(arguments.key))
        if arguments.output_file != None:
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
    elif arguments.cipher == 'vigenere':
        if arguments.input_file != None:
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        new_text = vigenere(text, alphabet, arguments.key)
        if arguments.output_file != None:
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
elif arguments.type == 'decode':
    if arguments.cipher == 'caesar':
        if arguments.input_file != None:
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        new_text = caesar(text, alphabet, -int(arguments.key))
        if arguments.output_file != None:
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
    elif arguments.cipher == 'vigenere':
        if arguments.input_file != None:
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        reversed_key = list()
        for i in range(len(arguments.key)):
           reversed_key.append(alphabet[(len(alphabet) - alphabet.index(arguments.key[i])) % len(alphabet)])
        reversed_key = ''.join(reversed_key)
        new_text = vigenere(text, alphabet, reversed_key)
        if arguments.output_file != None:
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
elif arguments.type == 'train':
    if(arguments.text_file != None):
        text = take_out_of_file(arguments.text_file)
    else:
        text = str(input())
    info = statistic(text, alphabet_lower)
    put_into_file(arguments.model_file, ' '.join(info))
elif arguments.type == 'hack':
    if arguments.input_file != None:
        text = take_out_of_file(arguments.input_file)
    else:
        text = str(input())
    difference = list()
    model = take_out_of_file(arguments.model_file)
    model = model.split(' ')
    text_info = statistic(text, alphabet_lower)
    for i in range(len(alphabet_lower)):
        model[i] = float(model[i])
        text_info[i] = float(text_info[i])
    for i in range(len(alphabet_lower)):
        difference.append(0)
        for a in range(len(alphabet_lower)):
            difference[i] += abs(model[a] - text_info[a])
        for a in range(len(alphabet_lower)):
            helper = text_info[(a+1)%len(alphabet_lower)]
            text_info[(a+1)%len(alphabet_lower)] = text_info[a]
    correct = min(difference)
    key = difference.index(correct)
    new_text = caesar(text, alphabet, key)
    if(arguments.output_file != None):
        put_into_file(arguments.output_file, new_text)
    else:
        print(new_text)
