class ProgramacionDinamica_FuerzaTrabajo:
    def __init__(self, weeks, workers_min, cost_excess, cost_hiring):
        """
        Inicializa la clase con los parámetros del problema.

        weeks: Número total de semanas a optimizar
        workers_min: Lista con el número mínimo de trabajadores requeridos por semana
        cost_excess: Costo por trabajador excedente por semana
        cost_hiring: Tupla con (costo fijo de contratación, costo por trabajador contratado)
        """
        self.weeks = weeks
        self.workers_min = workers_min
        self.cost_excess = cost_excess
        self.cost_hiring = cost_hiring
        self.memo = {}  # Diccionario para memoización

    def run(self):
        """
        Realiza la optimización de la fuerza de trabajo y escribe los resultados en un archivo.

        :return: Tupla con (costo total de la optimización, lista de decisiones óptimas)
        """
        cost_total = 0
        chosen = []
        workers_prev = 0

        # Abre el archivo para escribir los resultados
        with open("ProgramacionDinamica_FuerzaTrabajo - tarea.txt", "w", encoding="utf-8") as archivo:
            archivo.write("Resultados de la optimización del tamaño de la fuerza de trabajo:\n\n")

            for weekI in range(self.weeks):
                # Obtiene la decisión óptima para la semana actual
                cost, workers = self._optimize_week(weekI, workers_prev)
                cost_current = self._calcular_costo(weekI, workers_prev, workers)
                cost_total += cost_current
                chosen.append(workers)

                self._persist(archivo, weekI, workers, workers_prev, cost_current)
                workers_prev = workers

            # Escribe el costo total de la optimización
            archivo.write(f"Costo total de la optimización: ${cost_total:.2f}\n")

        return cost_total, chosen

    def _optimize_week(self, week, workers_prev):
        """
        Función recursiva para encontrar la decisión óptima para cada semana.
        """
        # Caso base: última semana
        if week == self.weeks - 1:
            return self._calcular_costo(week, workers_prev, self.workers_min[week]), self.workers_min[week]

        # Verifica si ya se ha calculado este estado (memoización)
        if (week, workers_prev) in self.memo:
            return self.memo[(week, workers_prev)]

        _cost_min = float('inf')
        best_choice = 0

        # Prueba todas las opciones posibles de fuerza de trabajo
        for workers in range(self.workers_min[week], max(self.workers_min) + 1):
            cost_current = self._calcular_costo(week, workers_prev, workers)
            cost_next_week, _ = self._optimize_week(week + 1, workers)
            cost_total = cost_current + cost_next_week

            # Actualiza la mejor decisión si se encuentra un costo menor
            if cost_total < _cost_min:
                _cost_min = cost_total
                best_choice = workers

        # Guarda el resultado en la memoria (memoización)
        self.memo[(week, workers_prev)] = (_cost_min, best_choice)
        return _cost_min, best_choice

    def _calcular_costo(self, week, workers_prev, workers_current):
        """
        Calcula el costo de una decisión específica.
        """
        cost = 0
        # Costo por exceso
        if workers_current > self.workers_min[week]:
            cost += (workers_current - self.workers_min[week]) * self.cost_excess
        # Costo por contratación
        if workers_current > workers_prev:
            cost += self.cost_hiring[0] + (workers_current - workers_prev) * self.cost_hiring[1]
        return cost

    def _persist(self, file_handler, week, workers, workers_prev, cost):
        """
        Escribe los resultados de una semana en el archivo.
        """
        file_handler.write(f"Semana {week + 1}:\n")
        file_handler.write(f"-- Trabajadores mínimos: {self.workers_min[week]}\n")
        file_handler.write(f"-- Trabajadores óptimos: {workers}\n")
        file_handler.write(f"-- Costo: $ {cost:.2f}\n")

        if workers > workers_prev:
            file_handler.write(f"-- Decisión: Contratar {workers - workers_prev} trabajadores\n")
        elif workers < workers_prev:
            file_handler.write(f"-- Decisión: Despedir {workers_prev - workers} trabajadores\n")
        else:
            file_handler.write("-- Decisión: Mantener el nro. de trabajadores actual\n")

        file_handler.write("\n")

if __name__ == "__main__":
    semanas = 5
    trabajadores_minimos = [5, 7, 8, 4, 6]
    costo_exceso = 300
    # (costo fijo, costo por trabajador
    costo_contratacion = (400, 200) 

    optimizador = ProgramacionDinamica_FuerzaTrabajo(semanas, trabajadores_minimos, costo_exceso, costo_contratacion)
    
    costo_total, trabajadores_optimos = optimizador.run()

    # Impresión de los resultados
    print(f"=== Costo total de la optimización: $ {costo_total:.2f}")
    print(f"=== Trabajadores óptimos por semana: {trabajadores_optimos}")