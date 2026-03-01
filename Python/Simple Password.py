while True:
  senha = input("Digite uma senha:")
  if len(senha) > 5 and len(senha) < 10:
    if any(c.isupper() for c in senha):
      if any(c.isdigit() for c in senha):
        break
      else:
        print("Digite sua senha com números")
    else:
      print("Sua senha precisa estar em maiúscula")
  else:
    print("Sua senha está muito curta")