import random
from numpy import vectorize


class GeneticAlgo:
    def __init__(self, hash_map, start, steps=5, crossover_prob=0.15, mutation_prob=0.15, population_size=5, iterations=100):
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.population_size = population_size
        self.hash_map = hash_map
        self.steps = steps
        self.iterations = iterations
        self.start = start
        self.cities = [k for k in self.hash_map.keys()]
        self.cities.remove(start)
        self.genes = []
        self.epsilon = 1 - 1 / self.iterations
        self.generate_genes = vectorize(self.generate_genes)
        self.evaluate_fitness = vectorize(self.evaluate_fitness)
        self.evolve = vectorize(self.evolve)
        self.prune_genes = vectorize(self.prune_genes)
        self.converge = vectorize(self.converge)

        self.generate_genes()

    def generate_genes(self):
        for i in range(self.population_size):
            gene = [self.start]
            options = [k for k in self.cities]
            while len(gene) < len(self.cities) + 1:
                city = random.choice(options)
                loc = options.index(city)
                gene.append(city)
                del options[loc]
            gene.append(self.start)
            self.genes.append(gene)
        return self.genes

    def evaluate_fitness(self):
        fitness_scores = []
        for gene in self.genes:
            total_distance = 0
            for idx in range(1, len(gene)):
                city_b = gene[idx]
                city_a = gene[idx - 1]
                try:
                    dist = self.hash_map[city_a][city_b]
                except:
                    dist = self.hash_map[city_b][city_a]
                total_distance += dist
            fitness = 1 / total_distance
            fitness_scores.append(fitness)
        return fitness_scores

    def evolve(self):
        index_map = {i: '' for i in range(len(self.cities))}
        indices = [i for i in range(len(self.cities))]
        to_visit = [c for c in self.cities]
        cross = (1 - self.epsilon) * self.crossover_prob
        mutate = self.epsilon * self.mutation_prob
        crossed_count = int(cross * len(self.cities))
        mutated_count = int((mutate * len(self.cities)) / 2)
        for idx in range(len(self.genes)):
            gene = self.genes[idx]
            for i in range(crossed_count):
                try:
                    gene_index = random.choice(indices)
                    sample = gene[gene_index]
                    if sample in to_visit:
                        index_map[gene_index] = sample
                        loc = indices.index(gene_index)
                        del indices[loc]
                        loc = to_visit.index(sample)
                        del to_visit[loc]
                    else:
                        continue
                except:
                    pass
        last_gene = self.genes[-1]
        remaining_cities = [c for c in last_gene if c in to_visit]
        for k, v in index_map.items():
            if v != '':
                continue
            else:
                city = remaining_cities.pop(0)
                index_map[k] = city
        new_gene = [index_map[i] for i in range(len(self.cities))]
        new_gene.insert(0, self.start)
        new_gene.append(self.start)
        for i in range(mutated_count):
            choices = [c for c in new_gene if c != self.start]
            city_a = random.choice(choices)
            city_b = random.choice(choices)
            index_a = new_gene.index(city_a)
            index_b = new_gene.index(city_b)
            new_gene[index_a] = city_b
            new_gene[index_b] = city_a
        self.genes.append(new_gene)

    def prune_genes(self):
        for i in range(self.steps):
            self.evolve()
        fitness_scores = self.evaluate_fitness()
        for i in range(self.steps):
            worst_gene_index = fitness_scores.index(min(fitness_scores))
            del self.genes[worst_gene_index]
            del fitness_scores[worst_gene_index]
        return max(fitness_scores), self.genes[fitness_scores.index(max(fitness_scores))]

    def converge(self):
        all_scores = set()
        best_gene = None
        for i in range(self.iterations):
            values = self.prune_genes()
            current_score = values[0]
            best_gene = values[1]
            self.epsilon -= 1 / self.iterations
            if i % 100 == 0:
                all_scores.add(int(1/current_score))

        return best_gene, all_scores
