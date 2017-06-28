import time
import subprocess as sp
import random

class Field:
  def __init__(self, ancho, largo):
    self.ancho = ancho
    self.alto = largo
    self.mundo = self.generar_mundo()
    self.comida = 0
    
  
  def print_field(self):
    screen = ""
    for y in range(self.alto):
      for x in range(self.ancho):
        screen += self.mundo[y][x].caracter
      screen += "\n"
    print screen

  def limpiar(self):
    for y in range(self.alto):
      for x in range(self.ancho):
        if (self.mundo[y][x].tipo == 'alimento' and self.mundo[y][x].alimento <= 0):
          self.posicionar_elemento([x, y], Nothing())
  
  def generar_mundo(self):
    mundo = []
    for y in range(self.alto):
      fila = []
      for x in range(self.ancho):
        if (random.randint(1,15) == 1):
          bush = Bush()
          bush.set_posicion(x, y)
          fila.append(bush)
        
        elif (random.randint(5,20) == 1):
          rock = Rock()
          rock.set_posicion(x, y)
          fila.append(rock)
        else:
          fila.append(Nothing())
      mundo.append(fila)  
    return mundo
  
  def posicionar_elemento(self, posicion, elemento):
    self.mundo[posicion[1]][posicion[0]] = elemento
  
  def mover_elemento(self, elemento, nueva_pos):
    if (elemento.posicion == nueva_pos):
      return False
    #comprobamos que se quiere mover dentro del mundo
    if (nueva_pos[0] < self.ancho and nueva_pos[0] >= 0 and nueva_pos[1] < self.alto and nueva_pos[1] >= 0 ):
      #comprobamos si podemos pasar por encima del elemento actual
      if (self.mundo[nueva_pos[1]][nueva_pos[0]].pisable):
        self.mundo[elemento.posicion[1]][elemento.posicion[0]] = Nothing()
        self.posicionar_elemento(nueva_pos, elemento)
        elemento.set_posicion(nueva_pos[0], nueva_pos[1])
        return True
    return False
    
    

class Man:
  def __init__(self, nombre):
    self.vida = 100
    self.caracter = '0'
    self.posicion = [0,0]
    self.pisable = False
    self.max_busqueda = 2
    self.material = {"material": "nada", "cantidad": 0}
    self.tipo = 'personaje'
    self.nombre = nombre
    self.pos_mem = False
    self.accion = "nada"
    self.parado = 0
    self.max_carga = 10
    
  def set_posicion(self, x, y):
    self.posicion = [x, y]
    
  def buscar_comida(self, mundo):
    direccion = []
    posibles = []
    
    for busqueda in range(1, self.max_busqueda+1):
      for x in range(self.posicion[0]-busqueda, self.posicion[0]+busqueda+1):
        for y in range(self.posicion[1]-busqueda, self.posicion[1]+busqueda+1):
          if (x < mundo.ancho and x >= 0 and y < mundo.alto and y >= 0 and self.posicion != [x, y]):
            if (mundo.mundo[y][x].tipo == 'alimento'):
              posibles.append((x,y))
      
      if (len(posibles) > 0):
        pos_comida = random.choice(posibles)
        
        direccion = [self.posicion[0] - pos_comida[0], self.posicion[1] - pos_comida[1]]
        direccion[0] = -1 if direccion[0] > 0 else 1
        direccion[1] = -1 if direccion[1] > 0 else 1
        return direccion
    
    return False
      
    
  def recoger_comida(self, mundo):
    posibles = []
    for x in range(self.posicion[0]-1, self.posicion[0]+2):
      for y in range(self.posicion[1]-1, self.posicion[1]+2):
        if (x < mundo.ancho and x >= 0 and y < mundo.alto and y >= 0 and self.posicion != [x, y]):
          if (mundo.mundo[y][x].tipo == 'alimento'):
            posibles.append((x,y))
    
    if (len(posibles) > 0):
      pos_comida = random.choice(posibles)
      mundo.mundo[pos_comida[1]][pos_comida[0]].alimento -= 3
      self.material['material'] = 'comida'
      self.material['cantidad'] += 3 
      return True
    else:
      return False
    
  def comer(self, mundo):
    if mundo.comida > 0:
      mundo.comida -= 1
      self.vida += 3
  
  def realizar_accion(self, almacen, mundo, group):
    direccion = [0, 0]
    if self.accion == 'nada':
      self.accion = 'recoger_comida'
    elif self.accion == 'recoger_comida':
      if self.recoger_comida(mundo):
        direccion = [0, 0]
        if self.material['material'] == 'comida' and self.material['cantidad'] >= self.max_carga:
          self.accion = 'descargar_warehouse'
          self.pos_mem = self.posicion
      else:
        direccion = self.buscar_comida(mundo)
        if direccion == False:
          direccion = [random.randint(-1,1), random.randint(-1,1)]
    elif self.accion == 'descargar_warehouse':
      if self.descargar_material(almacen):
        direccion = [0, 0]
        if self.pos_mem:
          self.accion = 'volver'
        else:
          self.accion = 'nada'
        
      else:
        direccion = self.buscar_almacen(almacen, mundo)
    elif self.accion == 'volver':
      direccion = calcular_direccion(self.posicion, self.pos_mem, 1)
      if direccion == [0, 0]:
        self.accion = 'nada'
    elif self.accion == 'reproducirse':
      almacen.materiales['comida'] -= 100
      self.reproducirse(group)
      self.accion = 'nada'
                
    self.moverse(mundo, direccion)
    
        
  def descargar_material(self, almacen):
    x = self.posicion[0] - almacen.posicion[0]
    y = self.posicion[1] - almacen.posicion[1]
    #print x, y
    if x <= 1 and x >= -1 and y <= 1 and y >= -1:
      almacen.materiales[self.material['material']] += self.material['cantidad']
      self.material['material'] = 'nada'
      self.material['cantidad'] = 0
      return True
    else:
      return False
    
    
    
    
  def buscar_almacen(self, almacen, mundo):
    direccion = calcular_direccion(self.posicion, almacen.posicion, 1)
    return direccion
    
  #def ir_almacen(self, almacen, mundo):
  #  direccion = calcular_direccion(self.posicion, almacen.posicion, 1)
  #  nueva_pos = [self.posicion[0] + direccion[0], self.posicion[1] + direccion[1]]
  #  mundo.mover_elemento(tete, nueva_pos)
  
  def moverse(self, mundo, direccion):
    nueva_pos = [self.posicion[0]+direccion[0], self.posicion[1]+direccion[1]]
    mov = mundo.mover_elemento(self, nueva_pos)
    
    #si no se ha movido se suma un turno a parado, si se ha movido se pone a 0
    if not mov:
      self.parado +=1
    else:
      self.parado = 0

    #print self.parado
    if self.parado >= 10: #si lleva 10 turnos sin moverse reseteamos la accion
      direccion = [random.randint(-1,1), random.randint(-1,1)]
      self.moverse(mundo, direccion)
      #self.accion = 'nada' 
      #self.parado = 0
    
    
class Nothing:
  def __init__(self):
    self.caracter = '.'
    self.pisable = True
    self.tipo = 'nada'
    
class Rock:
  def __init__(self):
    self.caracter = 'R'
    self.pisable = False
    self.position = [0, 0]
    self.tipo = 'nada'

  def set_posicion(self, x, y):
    self.posicion = [x, y]
 
class Bush:
  def __init__(self):
    self.caracter = 'B'
    self.pisable = False
    self.position = [0, 0]
    self.alimento = 50
    self.tipo = 'alimento'

  def set_posicion(self, x, y):
    self.posicion = [x, y]

class Warehouse:
  def __init__(self):
    self.caracter = 'W'
    self.pisable = False
    self.position = [0, 0]
    self.tipo = "edificio"
    self.materiales = {"comida": 0, "madera": 0}
    
  def meter_material(self, material, cantidad):
    self.materiales[material] += cantidad
    
    
  def sacar_material(self, material, cantidad):
    carrito = 0
    if self.materiales[material] >= cantidad:
      self.materiales[material] -= cantidad
      carrito = cantidad
    else:
      carrito = self.materiales[material]
      self.materiales[material] = 0
      
    return carrito

  def nuevo_hombre(self, group):
    global num_tetes
    if self.materiales['comida'] >= 100 + (10*num_tetes):
      self.sacar_material('comida', 100 + (10*num_tetes))
      num_tetes += 1
      new_tete = Man("Tete" + str(num_tetes))
      new_tete.set_posicion(self.posicion[0]+1, self.posicion[1])
      group.append(new_tete)


def calcular_direccion(old_pos, new_pos, salto = 1):
  direccion = [new_pos[0] - old_pos[0], new_pos[1] - old_pos[1]]
  while direccion[0] > salto or direccion[0] < salto * -1:
    if direccion[0] > 0:
      direccion[0] -= 1
    else:
      direccion[0] += 1
  
  while direccion[1] > salto or direccion[1] < salto * -1:
    if direccion[1] > 0:
      direccion[1] -= 1
    else:
      direccion[1] += 1
  
  return direccion



################## GENESIS
tiempo = 0

mundo = Field(75, 35)
num_tetes = 0

num_tetes += 1
tete = Man("Tete" + str(num_tetes))
tete.set_posicion(mundo.ancho//2, mundo.alto//2)
#tete.set_posicion(0,0)
tete.accion = "nada"
tetes = []
tetes.append(tete)
warehouse = Warehouse()
warehouse.posicion = [tete.posicion[0]+1, tete.posicion[1]]
#warehouse.posicion = [mundo.ancho//2, mundo.alto//2]

#bush = Bush()
#bush.posicion = [10, 5]
#mundo.posicionar_elemento(bush.posicion, bush)


mundo.posicionar_elemento(tete.posicion, tete)
mundo.posicionar_elemento(warehouse.posicion, warehouse)


##########################

      
while 1==1:
  new_tetes = []
  # Pasan cosas
  tiempo += 1
  print "Tiempo: " + str(tiempo)
  print "Comida: " + str(warehouse.materiales['comida'])
  datos_imprimir = ""
  
  warehouse.nuevo_hombre(tetes)
  
  for tete in tetes:
    
    #tete.recoger_comida(mundo)
    #tete.comer(mundo) 
    #tete.reproducirse(tetes)
    
    
    tete.realizar_accion(warehouse, mundo, tetes)
    
    #dir_comida = tete.buscar_comida(mundo)
    
    #if (dir_comida):
    #  nueva_pos = [tete.posicion[0]+dir_comida[0], tete.posicion[1]+dir_comida[1]]
    #else:
    #  nueva_pos = [tete.posicion[0]+random.randint(-1,1), tete.posicion[1]+random.randint(-1,1)]
    
    #mundo.mover_elemento(tete, nueva_pos)
    datos_imprimir += "{nombre_tete}: {vida}HP - {accion}\n".format(nombre_tete = tete.nombre, vida = tete.vida, accion = tete.accion)
    
    #tete.vida -= 1
    if tete.vida > 0:
      new_tetes.append(tete)
    else:
      mundo.posicionar_elemento(tete.posicion, Nothing())

  tetes = new_tetes

  #Limpieza de pantalla e impresion
  mundo.limpiar()
  mundo.print_field()
  print datos_imprimir
  
  
  time.sleep(0.05)
  tmp = sp.call('clear',shell=True)
