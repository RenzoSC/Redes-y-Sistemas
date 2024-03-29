import requests
from datetime import date


def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"

months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]

class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays):
        if(len(holidays)>0):
            now = date.today()
            today = {
                'day': now.day,
                'month': now.month
            }

            holiday = next( # Busca el proximo feriado a partir de hoy
                (h for h in holidays if h['mes'] == today['month'] and h['dia'] > today['day'] or h['mes'] > today['month']),
                holidays[0]
            )

            self.loading = False
            self.holiday = holiday
        else:
            self.loading =False
            self.holiday= None

    def fetch_holidays(self):
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data)

    def render(self):
        if self.holiday == None:
            print("\nNo hay feriado guardado o encontrado con busqueda hecha previamente\n")
        elif self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'], self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])

    def fetch_holiday_by_type(self, tipo):
        if(tipo not in ["inamovible","trasladable","nolaborable","puente"]):
            print("El tipo que se busca tiene que ser uno de los siguientes: \n")
            print("inamovible | trasladable | nolaborable | puente")
            return
        response = requests.get(get_url(self.year))
        data = response.json()
        type_holidays = []
        for feriados in range(len(data)):
            if data[feriados]['tipo'] == tipo:
                type_holidays.append(data[feriados])
        self.set_next(type_holidays)
      
      
if __name__ == '__main__':
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    next_holiday.render()
    next_holiday.fetch_holiday_by_type("nolaborable")
    next_holiday.render()
