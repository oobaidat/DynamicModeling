""" state.py
    Contains the information of a state at a certain times tep
    """


class State:
    def __init__(self, t):
        """
            t = time step of the state
            predicates = a dictionary containing the predicates of the state
        """
        self.t = t
        self.predicates = {}

    def check_predicate(self, predicate):
        """
            checks whether a predicate exists within this state
        """
        return predicate in self.predicates

    def get_predicate(self, predicate):
        """
            returns the predicate (list of agent(s) with corresponding value(s)) of this state
        """
        if predicate in self.predicates:
            return self.predicates[predicate]
        else:
            print("warning:", predicate, "predicate not found")

    def get_predicate_by_agent(self, predicate, agent, index=0):
        """
        returns a list of all predicate entries with a certain agent at the given index
        """
        output = []
        for entry in self.predicates[predicate]:
            if agent == entry.agents[index]:
                output.append(entry)
        return output

    def add_predicate_to_state(self, predicate_name, predicate_info):
        """
        adds a predicate to a state
        """
        self.predicates[predicate_name] = predicate_info

    def add_nested_predicate_to_state(self, nest_name, predicate_name, predicate_info):
        """
        adds a nested predicate to a state (predicate_name predicate under the nest_name predicate)
        """
        if nest_name in self.predicates:
            self.predicates[nest_name].value[predicate_name] = predicate_info
        else:
            self.predicates[nest_name] = Predicate("nested", {})
            self.predicates[nest_name].value[predicate_name] = predicate_info

    def retrieve_observations(self):
        """
        retrieves all observations of a state
        """
        if "observed" in self.predicates:
            return self.predicates["observed"].value
        else:
            return False

    def retrieve_beliefs(self):
        """
        retrieves all beliefs of a state
        """
        if "belief" in self.predicates:
            return self.predicates["belief"].value
        else:
            return False

    def retrieve_assessments(self):
        """
        retrieves all assessments of a state
        """
        if "assessment" in self.predicates:
            return self.predicates["assessment"].value
        else:
            return False

    def get_nested_predicate_by_name(self, nest, predicate_name, agent, index=0):
        """
        retrieve a nested predicate from a state by agent name (predicate_name predicate under the nest_name predicate)
        """
        if predicate_name in self.predicates[nest].value:
            output = []
            for entry in self.predicates[nest].value[predicate_name]:
                if agent == entry.agents[index]:
                    output.append(entry)
            return output
        else:
            return []


    def get_nested_predicate(self, nest, predicate_name):
        """
            returns the nested predicate (list of agent(s) with corresponding value(s)) of this state
        """
        if predicate_name in self.predicates[nest].value:
            return self.predicates[nest].value[predicate_name]
        else:
            print("warning:", nest, " ", predicate_name, " predicate not found")


    def check_belief_in_beliefs(self, predicate_name):
        """
        checks whether a belief is in the beliefs of a state
        """
        return predicate_name in self.predicates["belief"].value


class Predicate:
    def __init__(self, agents, value):
        self.agents = agents
        self.value = value

    def print(self):
        return str(self.agents) + str(self.value)
