#!/usr/bin/env python3
import sys
import argparse
import string

def statistic(text, alphabet):
    alphabet_size = len(alphabet)
    stats = list()
    summ = 0
    for i in range(alphabet_size):
        stats.append(0)
    for i in text:
        if i.lower() in alphabet:
            stats[alphabet.index(i.lower())] += 1
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
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser('encode')
    parser_encode.set_defaults(mode = 'encode')
    parser_encode.add_argument('--cipher')
    parser_encode.add_argument('--key')
    parser_encode.add_argument('--input-file')
    parser_encode.add_argument('--output-file')

    parser_decode = subparsers.add_parser('decode')
    parser_decode.set_defaults(mode = 'decode')
    parser_decode.add_argument('--cipher')
    parser_decode.add_argument('--key')
    parser_decode.add_argument('--input-file')
    parser_decode.add_argument('--output-file')

    parser_hack = subparsers.add_parser('hack')
    parser_hack.set_defaults(mode = 'hack')
    parser_hack.add_argument('--cipher')
    parser_hack.add_argument('--input-file')
    parser_hack.add_argument('--output-file')
    parser_hack.add_argument('--model-file')

    parser_train = subparsers.add_parser('train')
    parser_train.set_defaults(mode = 'train')
    parser_train.add_argument('--text-file')
    parser_train.add_argument('--output-file')

    return parser.parse_args()

def caesar(text, alphabet, key):
    alphabet_size = len(alphabet)
    key = key % alphabet_size
    new_text = list()
    for i in text:
        if i in alphabet:
            letter_number = alphabet.index(i)
            letter_number += key
            if letter_number >= alphabet_size:
                letter_number -= alphabet_size
            new_text.append(alphabet[letter_number])
        else:
            new_text.append(i)
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

def reversed_key(alphabet, key):
    reversed_key = list()
    for i in range (len(key)):
        reversed_key.append(alphabet[(len(alphabet) - alphabet.index(key[i])) % len(alphabet)])
    return ''.join(reversed_key)


alphabet = string.ascii_letters
alphabet_lower = string.ascii_lowercase
arguments = all_args()
if arguments.mode == 'encode' or arguments.mode == 'decode':
    if arguments.input_file != None:
        text = take_out_of_file(arguments.input_file)
    else:
        text = str(input())
    if arguments.cipher == 'caesar' and arguments.mode == 'encode':
        new_text = caesar(text, alphabet, int(arguments.key))
    elif arguments.cipher == 'caesar' and arguments.mode == 'decode':
        new_text = caesar(text, alphabet, -int(arguments.key))
    elif arguments.cipher == 'vigenere' and arguments.mode == 'encode':
        new_text = vigenere(text, alphabet, arguments.key)
    elif arguments.cipher == 'vigenere' and arguments.mode == 'decode':
        new_key = reversed_key(alphabet, arguments.key)
        new_text = vigenere(text, alphabet, new_key)
    if arguments.output_file != None:
        put_into_file(arguments.output_file, new_text)
    else:
        print(new_text)
elif arguments.mode == 'train':
    if(arguments.text_file != None):
        text = take_out_of_file(arguments.text_file)
    else:
        text = str(input())
    info = statistic(text, alphabet_lower)
    put_into_file(arguments.model_file, ' '.join(info))
elif arguments.mode == 'hack':
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
