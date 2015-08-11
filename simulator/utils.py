'''
Created on 6/7/2015
@author: Raul
'''
from constants import STEREOTYPE_RECIPES_PATH
import glob

'''Utility method to clean and provide a better format to user stereotype recipes from results
collected in Impala queries and matlab fittings'''
def build_stereotype(markov_chain_directory, interarrival_fittings_file):

    interarrivals = open(interarrival_fittings_file, "r")

    for markov_chain_file in sorted(glob.glob(markov_chain_directory + "*.csv")):
        output_markov_chain = file(STEREOTYPE_RECIPES_PATH + markov_chain_file.split("_")[-1].split(".")[0] + ".txt", "w")
        first_line = True
        for mc_line in open(markov_chain_file, "r"):
            if first_line:
                first_line = False
                continue

            state1, state2, num_transitions, mean_transition_time = mc_line.split(",")
            print markov_chain_file.split("_")[-1].split(".")[0], state1, state2
            interarrival_line = interarrivals.readline()[:-1]
            print interarrival_line
            fitting, parameters = interarrival_line.split(",")
            if fitting == "generalized extreme value": fitting = "genextreme"
            if fitting == "birnbaumsaunders": fitting = "fatiguelife"
            if fitting == "lognormal": fitting = "lognorm"
            if fitting == "generalized pareto": fitting = "genpareto"
            if fitting == "inversegaussian": fitting = "invgauss"

            print >> output_markov_chain, state1 + "," + state2 + "," + num_transitions + "," + fitting + "," + parameters

        output_markov_chain.close()

    interarrivals.close()


if __name__ == '__main__':
    build_stereotype("D:/Documentos/Recerca/Publicaciones/2015/user_stereotypes/Stereotype_Analysis/markov_chains/",
                     "D:/Documentos/Recerca/Publicaciones/2015/user_stereotypes/Stereotype_Analysis/data/interarrivals_fittings.txt")