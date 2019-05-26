import pytesseract as ocr
import cv2

def quebra():
	imagem = cv2.imread('img.jpg')
	imagem = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
	imagem = cv2.blur(imagem,(5,5))
	#cv2.imwrite("temp.jpg", imagem)

	#frase = ocr.image_to_string(imagem, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 6")
	frase = ocr.image_to_string(imagem, config="--psm 13")
	frase = frase[0:4]
	print(frase)

	return frase