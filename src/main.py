from textnode import *
from htmlnode import *

def main():
    tn = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
    print(tn)
                

main()