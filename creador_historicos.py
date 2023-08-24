import pandas as pd

base = pd.DataFrame(columns = ['Goles', 'Más de ', 'Menos de ','Partido', 'Liga', 'Hora de Recolección', 'Día de Recolección', 'Mes',
                    'Día', 'Hora'])

base.to_csv('historico_playdoit.csv')
base.to_csv('historico_codere.csv')