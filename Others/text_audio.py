from gtts import gTTS


def text_audio(text):
	gTTS(text).save('book_text_audio.mp3')
	

book = open('book.txt', 'r')

text_audio(book.read())
