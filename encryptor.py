#!/usr/bin/env python3
import sys
import argparse

def statistic(text):
    stats = list()
    summ = 0
    for i in range(26):
        stats.append(0)
    for i in range(len(text)):
        if(text[i].isalpha()):
            stats[ord(text[i].lower()) - ord('a')] += 1
            summ += 1
    for i in range(26):
        stats[i] /= summ
        stats[i] = str(stats[i])
    line = ' '.join(stats)
    return line
def take_out_of_file(given_file):
    text_file = open(given_file, 'r')
    text = ''.join([line for line in text_file])
    text_file.close()
    return text
def put_into_file(given_file, text):
    text_file = open(given_file, 'w')
    text_file.write(text)
    text_file.close()
parser = argparse.ArgumentParser()
parser.add_argument('type')
parser.add_argument('--cipher')
parser.add_argument('--key')
parser.add_argument('--input-file')
parser.add_argument('--output-file')
parser.add_argument('--text-file')
parser.add_argument('--model-file')
arguments = parser.parse_args(sys.argv[1:])
if(arguments.type == 'encode'):
    if(arguments.cipher == 'caesar'):
        key = int(arguments.key) % 26
        if(arguments.input_file != None):
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        new_text = ''
        for i in range(len(text)):
           if(ord(text[i]) > 64 and ord(text[i]) < 91):
               new_ASCII = ord(text[i]) + key
               if(new_ASCII > 90):
                   new_ASCII -= 26
               new_text += chr(new_ASCII)
           elif(ord(text[i]) > 96 and ord(text[i]) < 123):
               new_ASCII = ord(text[i]) + key
               if(new_ASCII > 122):
                   new_ASCII -= 26
               new_text += chr(new_ASCII)
           else:
               new_text += text[i]
        if(arguments.output_file != None):
            put_into_file(arguments.output_file, new_text)
        else:
            print(text)
    elif(arguments.cipher == 'vigenere'):
        key = arguments.key
        if(arguments.input_file != None):
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        working_key = key.lower()
        new_text = ''
        while (len(working_key) < len(text)):
            working_key += key.lower()
        for i in range(len(text)):
            digit_key = ord(working_key[i]) - ord('a')
            if(ord(text[i]) > 64 and ord(text[i]) < 91):
                new_ASCII = ord(text[i]) + digit_key
                if(new_ASCII > 90):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            elif(ord(text[i]) > 96 and ord(text[i]) < 123):
                new_ASCII = ord(text[i]) + digit_key
                if(new_ASCII > 122):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            else:
                new_text += text[i]
        if(arguments.output_file != None):
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
elif(arguments.type == 'decode'):
    if(arguments.cipher == 'caesar'):
        key = (int(arguments.key) * -1) % 26
        if(arguments.input_file != None):
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        new_text = ''
        for i in range(len(text)):
           if(ord(text[i]) > 64 and ord(text[i]) < 91):
               new_ASCII = ord(text[i]) + key
               if(new_ASCII > 90):
                   new_ASCII -= 26
               new_text += chr(new_ASCII)
           elif(ord(text[i]) > 96 and ord(text[i]) < 123):
               new_ASCII = ord(text[i]) + key
               if(new_ASCII > 122):
                   new_ASCII -= 26
               new_text += chr(new_ASCII)
           else:
               new_text += text[i]
        if(arguments.output_file != None):
               put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
    if(arguments.cipher == 'vigenere'):
        key = arguments.key
        if(arguments.input_file != None):
            text = take_out_of_file(arguments.input_file)
        else:
            text = str(input())
        working_key = key.lower()
        new_text = ''
        while(len(working_key) < len(text)):
            working_key += key.lower()
        for i in range(len(text)):
            digit_key = ((ord(working_key[i]) - ord('a')) * -1) % 26
            if(ord(text[i]) > 64 and ord(text[i]) < 91):
                new_ASCII = ord(text[i]) + digit_key
                if(new_ASCII > 90):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            elif(ord(text[i]) > 96 and ord(text[i]) < 123):
                new_ASCII = ord(text[i]) + digit_key
                if(new_ASCII > 122):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            else:
                new_text += text[i]
        if(arguments.output_file != None):
            put_into_file(arguments.output_file, new_text)
        else:
            print(new_text)
elif(arguments.type == 'train'):
    if(arguments.text_file != None):
        text = take_out_of_file(arguments.text_file)
    else:
        text = str(input())
    info = statistic(text)
    put_into_file(arguments.model_file, info)
elif(arguments.type == 'hack'):
    if(arguments.input_file != None):
        text = take_out_of_file(arguments.input_file)
    else:
        text = str(input())
    difference = list()
    model = take_out_of_file(arguments.model_file)
    model = model.split(' ')
    for i in range(26):
        model[i] = float(model[i])
    for i in range(26):
        new_text = ''
        for a in range(len(text)):
            if(ord(text[a]) < 91 and ord(text[a]) > 64):
                new_ASCII = ord(text[a]) + 1
                if(new_ASCII > 90):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            elif(ord(text[a]) < 123 and ord(text[a]) > 96):
                new_ASCII = ord(text[a]) + 1
                if(new_ASCII > 122):
                    new_ASCII -= 26
                new_text += chr(new_ASCII)
            else:
                new_text += text[a]
        text = new_text
        stats = statistic(text).split(' ')
        for a in range(26):
            stats[a] = float(stats[a])
        difference.append(0)
        for a in range(26):
            difference[i] += abs(model[a] - stats[a])
    correct = min(difference)
    change = difference.index(correct)
    new_text = ''
    for i in range(len(text)):
        if(ord(text[i]) < 91 and ord(text[i]) > 64):
            new_ASCII = ord(text[i]) + change
            if(new_ASCII > 90):
                new_ASCII -= 26
            new_text += chr(new_ASCII)
        elif(ord(text[i]) < 123 and ord(text[i]) > 96):
            new_ASCII = ord(text[i]) + change
            if(new_ASCII > 122):
                new_ASCII -= 26
            new_text += chr(new_ASCII)
        else:
            new_text += text[i]
    if(arguments.output_file != None):
        put_into_file(arguments.output_file, new_text)
    else:
        print(new_text)
