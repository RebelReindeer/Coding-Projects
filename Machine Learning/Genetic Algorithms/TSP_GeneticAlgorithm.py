import math
import random as r
import pygame
import matplotlib.pyplot as plt


class city():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def pos(self):
    return(self.x, self.y)

  def distancefromcity(self, city2):
     temp = (city2.x - self.x)**2 + (city2.x - self.y)**2
     math.sqrt(temp)
     return round(temp, 2)

def makelocations(num_locations):
  citylist = []
  for i in range(num_locations):
    citylist.append(city(r.randint(1, num_locations*2), r.randint(1, num_locations*2)))
  return citylist

class genome():
  def __init__(self, dna):
    self.dna = dna
  def fitness(self):
    distance = 0
    for i in range(1, len(self.dna)):
      temp = locations[self.dna[i - 1]].distancefromcity(locations[self.dna[i]])
      distance += temp
    return round(distance, 2)

def create_initial_population():
  population = []
  for i in range(10):
    listt = [x for x in range(len(locations))]
    r.shuffle(listt)
    population.append(genome(listt))
  return population

NUM_LOCATIONS = 100
SCALER = 4


locations1 = [[23, 4], [27, 8], [35, 9], [34, 3], [38, 17], [36, 21], [38, 28], [37, 34], [32, 37], [24, 35], [15, 35], [10, 33], [8, 30], [4, 26], [3, 19], [7, 15], [7, 10], [13, 10], [18, 8], [21, 21]]

locations = []
for i in locations1:
  locations.append(city(i[0], i[1]))

locations = makelocations(NUM_LOCATIONS)
genomes = create_initial_population()
history = []
def crossover(p1, p2):
  crossoverpoint = r.randint(0, len(p1))
  baby1 = p1[crossoverpoint:] + [x for x in p2 if x not in p1[crossoverpoint:]]
  baby2 = p2[crossoverpoint:] + [x for x in p1 if x not in p2[crossoverpoint:]]

  baby11 = genome(baby1)
  baby22 = genome(baby2)

  mutation_rate = r.randint(0, len(p1) - 1)

  if mutation_rate % 2 == 0:

    temp1 = r.randint(0, len(baby1) - 1)
    temp2 = r.randint(0, len(baby1) - 1)
    baby1[temp1], baby1[temp2] = baby1[temp2], baby1[temp1]
    baby2[temp1], baby2[temp2] = baby2[temp2], baby2[temp1]

  return baby1, baby2

def genetic_algorithm(num_generations):
  pygame.font.init() 
  genomes = create_initial_population()
  

  pygame.init()
  clock = pygame.time.Clock()

  BLACK = (0, 0, 0)
  BLUE = (0, 0, 255)
  CYAN = (0, 255, 255)
  GREEN = (0, 255, 0)
  PURPLE = (255, 0, 255)
  RED = (255, 0, 0)
  WHITE = (255, 255, 255)

  #draw window
  win_width = 1000
  win_height = 1000
  wn = pygame.display.set_mode((win_width, win_height))
  pygame.display.set_caption('genetic algorithm')

  

  #plot initial solution
  i = 0

  state = True
  while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
        pygame.display.update()
        clock.tick(30)

        i += 1
        
        initial_population = []
        
        for j in genomes: 
            initial_population.append((j.dna, j.fitness()))

        initial_population = sorted(initial_population, key=lambda tup: tup[1], reverse = False)
        
        new_pop = []

        new_pop.append(genome(initial_population[0][0]))

        for j in range(len(initial_population)//2):
            new_pop.append(genome(crossover(initial_population[j][0], initial_population[j + 1][0])[0]))
            new_pop.append(genome(crossover(initial_population[j][0], initial_population[j + 1][0])[1]))

        new_pop_info = []

        for j in new_pop: new_pop_info.append((j.dna, j.fitness()))

        new_pop_info = sorted(new_pop_info, key = lambda tup: tup[1], reverse = False)

        del new_pop_info[-1]

        print(f'----- population {i} -----')
        print(f'best solution {new_pop_info[0]}')

        history.append(new_pop_info[0][1])

        #draw line from item 0  - item 1, item 1 to item 2...
        

        coords = []

        for _ in new_pop_info[0][0]:
            coords.append((locations[_].x * SCALER, locations[_].y * SCALER))
        
        for _ in locations:
            pygame.draw.circle(wn, WHITE, (_.x * SCALER, _.y * SCALER), 6)
        
        myfont = pygame.font.SysFont('arial', 30)
        myfont1 = pygame.font.SysFont('arial', 12)
        textsurface = myfont.render(f'distance: {new_pop_info[0][1]}', False, WHITE)
        textsurface1 = myfont1.render(f'solution: {new_pop_info[0][0]}', False, WHITE)
            

        
        wn.blit(textsurface,(10,800))
        wn.blit(textsurface1, (1, 850))

        
        pygame.draw.lines(wn, WHITE, False, coords)

     
        #coords.clear()
        
        if i % 10 == 0:
            wn.fill(BLACK)

        genomes = new_pop
    
  return history

a1 = genetic_algorithm(10000)
#algos = [genetic_algorithm(1000) for x in range(3)]

plt.title('Genetic Algorithm Fitness Improvement')
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.plot(a1)
# for i in algos:
#   plt.plot(i)
plt.autoscale(True)
plt.show()

print(f'Best Solution Found: {a1[-1]}')


pygame.quit()
