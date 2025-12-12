import calculations

# d1 = input ("Введите кратчайшее расстояние от спасателя до кромки воды (в ярдах) ")
# d2 = input ("Введите кратчайшее расстояние от утопающего до берега (в футах) ")
# h = input ("Введите боковое смещение между спасателем и утопающим (в ярдах) ")
# vsand = input ("Введите скорость движения спасателя по песку (в милях в час) ")
# n = input ("Введите коэффициент замедления спасателя при движении в воде ")
# th = input ("Введите направление движения спасателя по песку (в градусах) ")

# имитируем ввод значений пользователем (для целей тестирования)
d1 = "8"
d2 = "10"
h = "50"
vsand = "5"
n = "2"
th = "39.413"
print("Для заданных параметров 8, 10, 50, 5, 2, 39.413 ответ должен быть 39.9") #типа тест)))

def output (th, t):
    print(f"Если спасатель начнёт движение под углом theta1, равным {th:.0f} градусам, он достигнет утопащего через {t:.1f} (сек.)")
def optim_output (opt):
    print(f"А если спасатель начнёт движение под углом, равным {opt[0]:.0f} градусам, то он достигнет утопащего через {opt[1]:.1f} (сек.)")

output (float(th), calculations.calc(calculations.rearrange(d1, d2, h, vsand, n, th)))
if (round(calculations.calc(calculations.rearrange("8", "10", "50", "5", "2", "39.413"))) == round(39.87067379369796)):
     print("True")
else: print("False")

new_t = calculations.optimal(calculations.rearrange(d1, d2, h, vsand, n, th))
optim_output (new_t)
print("Проверяем подбор оптимального угла через предыдущую функцию (верны ли расчёты)") #ещё тест
if (round(calculations.calc(calculations.rearrange("8", "10", "50", "5", "2", new_t[0])))) == round(new_t[1]):
     print("True")
else: print("False")
    
    
    
    

