import cv2 as cv
import numpy as np
import argparse

def registraPonto(event, x, y, flag, parametros):
    pontos = parametros[0]
    img = parametros[1]
    if event == cv.EVENT_LBUTTONDOWN:
        if len(pontos) == 4:
            return
        pontos.append((x,y))
        cv.circle(img,  (x, y), 6, (0, 255, 0), -1)
        if len(pontos) > 1:
            cv.line(img, pontos[-2], pontos[-1], (255, 0, 0), 2)
        if len(pontos) == 4:
            cv.line(img, pontos[0], pontos[-1], (255, 0, 0), 2)
        cv.imshow("Selecione os 4 cantos (l para limpar)", img)



def calcTam(pontos):
    (se, sd, id, ie) = pontos
    largSup = np.sqrt(((sd[0] - se[0])**2) + ((sd[1] - se[1])**2))
    largInf = np.sqrt(((id[0] - ie[0])**2) + ((id[1] - ie[1])**2))
    largSaida = max(int(largSup), int(largInf))
    altDir = np.sqrt(((sd[0] - id[0])**2) +((sd[1] - id[1])**2))
    altEsq = np.sqrt(((se[0] - ie[0])**2) +((se[1] - ie[1])**2))
    altSaida = max(int(altEsq), int(altDir))
    return (largSaida, altSaida)



def transformaPerspectiva(img, pontos):
    (largSaida, altSaida) = calcTam(pontos)
    ptsSaida = [(0,0), (largSaida-1, 0), (largSaida-1, altSaida-1), (0, altSaida-1)]

    M = cv.getPerspectiveTransform(pontos, ptsSaida)
    imgTrans = cv.warpPerspective(img, M, (largSaida, altSaida))
    return imgTrans



def selecionaPotosInteresse(img):
    pts = []
    imgAux = img.copy()
    params = [pts, imgAux]
    cv.namedWindow("Selecione os 4 cantos (l para limpar)")
    cv.setMouseCallback("Selecione os 4 cantos (l para limpar)", registraPonto, params)

    while True:
        cv.imshow("Selecione os 4 cantos (l para limpar)", imgAux)
        key = cv.waitKey(1) & 0xFF
        if key == ord("l"):
            pts = []
            imgAux = img.copy()
        elif key == ord("c"):
            if len(pts) == 4:
                cv.destroyAllWindows()
                return pts
            print("Selecione os quatro cantos da area de interesse.")
        elif key == ord("q"):
            break
    cv.destroyAllWindows()
    return None



def ajuda():
    print("Instruções:")
    print("Selecione os 4 cantos da área de interesse na ordem:")
    print("1 - Canto Superior Esquerdo")
    print("2 - Canto Superior Direito")
    print("3 - Canto Inferior Direito")
    print("4 - Canto Inferior Esquerdo")
    print("Pressione 'c' para confirmar e prosseguir")
    print("Pressione 'l' para limpar os pontos selecionados")
    print("Pressione 'q' para Sair")



def main():

    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", required=True, help="Caminho para a imagem de entrada.")
    parse.add_argument("-o", "--output", default="resultado.png", help="Caminho para a imagem transformada (PNG).")
    args = parse.parse_args()
    caminhoImg = args.input
    img = cv.imread(caminhoImg)
    if img is None:
        print("Erro: Falha ao carregar a imagem. Saindo...")
        return
    ajuda()
    pts = selecionaPotosInteresse(img)
    if pts is None:
        print("Seleção cancelada. Saindo...")
        return
    imgTrans = transformaPerspectiva(img, pts)
    cv.imwrite(args.output, imgTrans)



if __name__ == "__main__":
    main()














