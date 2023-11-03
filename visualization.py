""" visualization.py
     for visualization
    """
from matplotlib import lines
from numpy import arange

import matplotlib.pyplot as plt


def make_visualization_dic(state_machine):
    visualization_dic = {}
    for state in state_machine.states:
        t = state.t
        predicates = state.predicates
        for predicate_name in predicates.keys():
            predicate = predicates[predicate_name]
            try:
                type(predicates[predicate_name].value)
            except AttributeError:
                # non-nested predicate
                visualization_dic = add_non_nested_predicate(predicate, predicate_name, visualization_dic, t)
            else:
                # nested predicate
                nested_predicates = predicates[predicate_name].value
                for nested_predicate_name in nested_predicates.keys():
                    nested_predicate = nested_predicates[nested_predicate_name]
                    nested_predicate_name = "%s_%s" % (predicate_name, nested_predicate_name)
                    visualization_dic = add_non_nested_predicate(nested_predicate, nested_predicate_name,
                                                                 visualization_dic, t)

    return visualization_dic


def add_non_nested_predicate(predicate, predicate_name, visualization_dic, t):
    for predicate_values in predicate:
        if predicate_values.agents is None:
            agent = None
        else:
            agent = tuple(predicate_values.agents) if len(predicate_values.agents) > 1 else predicate_values.agents[
                0]
        value = predicate_values.value
        visualization_dic = add_predicate_visualization(agent, value, predicate_name, visualization_dic, t)
    return visualization_dic


def add_predicate_visualization(agent, value, predicate_name, visual_dic, t):
    if predicate_name in visual_dic:
        if agent in visual_dic[predicate_name]:
            visual_dic[predicate_name][agent].append((t, value))
        else:
            visual_dic[predicate_name][agent] = [(t, value)]
    else:
        visual_dic[predicate_name] = {}
        visual_dic[predicate_name][agent] = [(t, value)]
    return visual_dic


def check_completeness(visual_dic, StateMachine):
    for predicate_name in visual_dic.keys():
        predicate = visual_dic[predicate_name]
        for agent in predicate.keys():
            if len(predicate[agent]) <= 1:
                for i in range(1, StateMachine.max_t):
                    visual_dic[predicate_name][agent].insert(i, (i+1, None))
            for i in range(0, StateMachine.max_t):
                t1 = i + 1
                t2 = visual_dic[predicate_name][agent][i][0]
                if t1 != t2:
                    visual_dic[predicate_name][agent].insert(i, (t1, None))
    return visual_dic


def create_lineplot(viz_dic, predicate_and_agent):
    data = viz_dic[predicate_and_agent[0]][predicate_and_agent[1]]
    fig, ax = plt.subplots()
    ax.plot(data, linewidth=2.0)
    ax.set_xlabel("Time Step")
    ax.set_ylabel("%s (%s)" % (predicate_and_agent[0], predicate_and_agent[1]), rotation='horizontal', ha='right')
    plt.margins(0)
    y_lim_min = min(y for y in data if y is not None)
    y_lim_max = max(y for y in data if y is not None) + (max(y for y in data if y is not None) / 100)
    plt.ylim([y_lim_min, y_lim_max])
    plt.tight_layout()
    plt.show()


def create_matgraph(viz_dic, predicate_to_plot, timesteps):
    """predicate to plot is Input has to be list of tuples with predicate name, agent, value to be verified
    i.e. [("has_emotion_state",'arnie', 'sad'), ("has_emotion_state",'arnie', 'indifferent')],
     maximum amount of timesteps to be inserted"""
    data = []
    for i in predicate_to_plot:
        list = [8]
        x = viz_dic[i[0]][i[1]]
        for j in x[:timesteps + 1]:
            if j[1] is None:
                list.append(8)
            elif j[1] == i[2]:
                list.append(1)
            else:
                list.append(0)
        data.append(list)
    d = [x for x in range(timesteps + 1)]
    plt.matshow(data, cmap="Pastel1", fignum=1, aspect='auto')
    plt.xlabel("Time Steps", labelpad=5)
    names = []
    for i in predicate_to_plot:
        names.append("%s\n(%s,%s)" % (i[0], i[1], str(i[2])))
    plt.yticks(arange(len(predicate_to_plot)), names)
    plt.xticks(arange(-0.5, timesteps, step=1), ha="right", labels=d)
    for i in range(len(predicate_to_plot)):
        plt.axhline(i + 0.5, color='k')
    plt.grid(axis='x', color='k')
    plt.show()


def run_visualization(StateMachine, plot_type, predicate_to_plot, time):
    """Input is the StateMachine, the plot type('line' or 'bar') and then what you want to plot as a list.
    If you wish to do a line plot then your list is one predicate and agent(you can only plot one at a time).
     Thus your list will be ['predicate name', 'agent' or agents(then in a tuple('agent1','agent2'). If you wish to
      make a true/false bar graph that can be done with as many inputs as you want and your input data
      must be in the following style: a list of tuples in each tuple you have ('predicate name', 'agent', 'and the
      value you are looking for') Example: [("has_emotion_state", 'arnie', 'happy'),("has_emotion_state", 'arnie', 'angry')]
      lastly for the true/false bar graph one must specify over how many timesteps you wish to see it(a positive integer)
      if you are doing a line plot put None"""
    visualization_dic = make_visualization_dic(StateMachine)
    visualization_dic = check_completeness(visualization_dic, StateMachine)
    if plot_type == 'line':
        create_lineplot(visualization_dic, predicate_to_plot)
    elif plot_type == 'bar':
        create_matgraph(visualization_dic, predicate_to_plot, time)
    else:
        print("Something went wrong")



