import os

def depurar(path):
    for file_name in os.listdir(path):

      file_path = os.path.join(path, file_name)

      # Verificar si es un archivo y si es eliminable
      if os.path.isfile(file_path) and os.access(file_path, os.W_OK):
        os.remove(file_path)
      elif os.path.isdir(file_path) and os.access(file_path, os.W_OK):
          depurar(file_path)

path = '/tmp'
depurar(path)