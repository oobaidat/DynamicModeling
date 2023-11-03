""" state_machine.py
    The state_machine is the force behind creating and defining each state
    """

from state import Predicate
from state import State
from visualization import run_visualization


class StateMachine:
    def __init__(self, scenario, max_t, rules, agents=True):
        """
            scenario = the scenario defined by the user
            max_t = the maximum time step the StateMachine will run to
            states = pre-made list of empty states
        """
        self.scenario = scenario
        self.max_t = max_t
        self.rules = rules
        self.states = self.create_states()
        self.agents = agents
        self.fill_states()

    def create_states(self):
        """
            create "max_t" number of empty states
            State(i + 1), because it ranges from 0 - max_t, but states start from 1
        """
        states = []
        for i in range(self.max_t):
            states.append(State(i + 1))
        return states

    def fill_states(self):
        """
            fill states based on solely the scenario file
        """
        predicates = open(self.scenario, "r").read().splitlines()
        for predicate in predicates:
            if predicate == "":
                break
            predicate = predicate.split(";")
            time_steps = predicate[-1]
            predicate = predicate[0]
            if self.agents:
                predicate, agent, value = self.filter_predicate_info(predicate)
                start_time, end_time = self.filter_predicate_time(time_steps)
                self.insert_predicate(predicate, agent, value, start_time, end_time)
            else:
                predicate, values = self.filter_predicate_info(predicate)
                start_time, end_time = self.filter_predicate_time(time_steps)
                self.insert_predicate(predicate, None, values, start_time, end_time)


    def run(self):
        """
            run all rules that are inside the rules.py file
        """
        for t in range(1, self.max_t):
            """
                execute all rules and create all predicates for state t
            """
            for rule in self.rules:
                rule(self.states[:t + 1], t)


    def filter_predicate_info(self, predicate):
        """
            filters predicate information from a predicate from the scenarios file
        """
        if self.agents:
            # if there are agents used in the predicates
            return self.filter_predicate_info_with_agents(predicate)
        else:
            # if there are no agents used in the predicates
            return self.filter_predicate_info_without_agents(predicate)


    @staticmethod
    def filter_predicate_info_with_agents(predicate):
        """
            filters predicate information from a predicate from the scenarios file
        """
        predicate = predicate.split("{")
        name_predicate = predicate[0]
        agent_and_value = predicate[-1]
        agent_and_value = agent_and_value.split(",")
        agents = agent_and_value[:-1]
        # delete whitespaces in names of agents in case of multiple agentsduuu
        agents = [agent.strip() for agent in agents]
        value = agent_and_value[-1].strip("}").strip(" ")
        # if the value is a real number, make it a float, in order to use it in the rules
        try:
            value = float(value)
        except ValueError:
            pass
        if len(predicate) == 3:
            name_predicate = [name_predicate, predicate[1]]
        return [name_predicate, agents, value]


    @staticmethod
    def filter_predicate_info_without_agents(predicate):
        """
            filters predicate information from a predicate from the scenarios file
        """
        predicate = predicate.split("{")
        name_predicate = predicate[0]
        values = predicate[-1]
        values = values.split(",")
        # make a list of the values
        values = [value.strip() for value in values]
        values[-1] = values[-1].strip("}")
        # if values is a single value make it a list
        if type(values) == str:
            values = [values]
        # if the value is a real number, make it a float, in order to use it in the rules
        for i, value in enumerate(values):
            try:
                value = float(value)
                values[i] = value
            except ValueError:
                pass
        if len(predicate) == 3:
            # nested predicate
            name_predicate = [name_predicate, predicate[1]]
        return [name_predicate, values]


    def filter_predicate_time(self, time):
        """
            filters predicate duration from a predicate from the scenarios file
            start_time = start_time - 1, since index starts from 0
        """
        time = time.split("[")
        time = (time[1].split("]"))[0]
        if len(time) == 1:
            # just 1 time point
            start_time, end_time = int(time[0]) - 1, int(time[0])
        else:
            # range of time points
            time = time.split(":")
            start_time = int(time[0]) - 1
            if time[-1].lower() == "inf":
                end_time = self.max_t
            else:
                end_time = int(int(time[-1]))
        return [start_time, end_time]

    def insert_predicate(self, predicate, agent, value, start_time, end_time):
        """
            insert the predicate to the corresponding states
        """
        for i in range(start_time, end_time):
            if type(predicate) != list:
                # single predicate
                if predicate in self.states[i].predicates:
                    # if the key is already in the dictionary, add a list of the agent + value to the key
                    self.states[i].predicates[predicate].append(Predicate(agent, value))
                else:
                    # if the key is not in the dictionary, create a list and add a list of the agent + value to the key
                    self.states[i].predicates[predicate] = [Predicate(agent, value)]
            else:
                # nested predicate
                if predicate[0] in self.states[i].predicates:
                    if predicate[1] in self.states[i].predicates[predicate[0]].value:
                        self.states[i].predicates[predicate[0]].value[predicate[1]].append(Predicate(agent, value))
                    else:
                        self.states[i].predicates[predicate[0]].value[predicate[1]] = [Predicate(agent, value)]
                else:
                    self.states[i].predicates[predicate[0]] = Predicate("nested", {})
                    self.states[i].predicates[predicate[0]].value[predicate[1]] = [Predicate(agent, value)]