'''
Created on 30/6/2015
@author: Raul
'''

from scipy import stats
import numpy

class InterArrivalsManager(object):

    def __init__(self):
        self.transition_interarrival_fittings = dict()

    '''Get the waiting time between operations based on the statistical fittings'''
    def get_waiting_time(self, state1, state2):
        (function, kv_params) = self.transition_interarrival_fittings[state1][state2]
        fitting = getattr(stats, function)
        if 'shape' in kv_params:
            return fitting(-kv_params['shape'], loc=kv_params['loc'], scale=kv_params['scale']).rvs()
        else: return fitting(**kv_params).rvs()

    def add_interarrival_transition_fitting(self, state1, state2, function, params):
        #If there is no entry for this transition, create one
        if state1 not in self.transition_interarrival_fittings:
            self.transition_interarrival_fittings[state1] = dict()
        if state2 not in self.transition_interarrival_fittings[state1]:
            self.transition_interarrival_fittings[state1][state2] = None
        self.transition_interarrival_fittings[state1][state2] = (function, params)

    '''Get the inter-arrival inforation from stereotype recipe'''
    def initialize_from_recipe(self, stereotype_recipe):
        for l in open(stereotype_recipe, "r"):
            state1, state2, num_transitions, fitting, raw_fitting_params = l[:-1].split(",")
            kw_params = dict()
            for param_tuple in raw_fitting_params[:-1].split(" "):
                print param_tuple
                k, v = param_tuple.split("=")
                kw_params[k] = float(v)
            self.add_interarrival_transition_fitting(state1, state2, fitting, kw_params)

if __name__ == '__main__':

    #genextreme,k=0.718044067607244 sigma=0.932804666751013 mu=1.20212649309532
    #print "EXPONENTIAL"    , 0.932804666751013, 1.20212649309532
    #rv = stats.genextreme(0, 0.932804666751013, 0.718044067607244,1.20212649309532)
    #shape, scale, loc = (2.99480920063372, 2.46709346372752, 0.0249999999999978)  #(1.0, 1.321950408033661, 0.85874898071806682) #(0.7180, 0.9328, 1.2021)
    #fitting = stats.lognorm(4.67861713792556, 6.91953608758707)
    '''generalized extreme OK
    lognormal OK
    birnbaumsaunders OK
    generalized pareto OK
    inversegaussian OK
    logistic NO
    loglogistic/fisk NO '''

    #v = numpy.random.gumbel(loc=1.20212649309532, scale=0.932804666751013, size=10000)
    #fitting = stats.genextreme(-0.718044067607244, loc=1.20212649309532, scale=0.932804666751013)
    #fitting = stats.lognorm(4.67861713792556, scale=6.91953608758707)
    #fitting = stats.invgauss(5.3146e+003, scale=0.9277)
    #fitting = stats.fatiguelife(18.1441, scale=359.6783)
    fitting = stats.fisk(0.4190, shape=0.5201)
    #mu=9.31524829249769 sigma=41.5219061720147 
    #fitting = stats.lognorm(0.8491, loc=-0.089)
    #fitting = stats.logistic(64.9711, shape=69.3347)
    #print stats.genpareto.fit(rvs)
    test = open("test.dat", "w")
    for i in range(10000):
        print >> test, fitting.rvs()
        #print stats.genpareto(2.9948, scale=2.4671, loc=0.0250).rvs()
        #c=[0.7180, 0.9328, 1.2021]
        #print stats.fisk.rvs(0.5201, 0.4190)
    test.close()
    '''STEREOTYPE_RECIPES_PATH = "D:/Documentos/Recerca/Publicaciones/2015/user_stereotypes/Stereotype_Analysis/"
    to_fit = []
    for line in open(STEREOTYPE_RECIPES_PATH + "/data/backup_GetContentResponse_GetContentResponse.dat", "r"):
        to_fit.append(float(line.split(",")[1])/1000.0)
        
    dist_names = ['genextreme', 'genpareto']
    
    for dist_name in dist_names:
        print dist_name
        dist = getattr(stats, dist_name)
        param = dist.fit(to_fit)
        print param'''

    '''import matplotlib.pyplot as plt
    import scipy
    import scipy.stats
    size = 30000
    x = scipy.arange(size)
    y = scipy.int_(scipy.round_(scipy.stats.vonmises.rvs(5,size=size)*47))
    h = plt.hist(y, bins=range(48), color='w')
    
    dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']
    
    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        param = dist.fit(y)
        pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
        plt.plot(pdf_fitted, label=dist_name)
        plt.xlim(0,47)
    plt.legend(loc='upper right')
    plt.show()'''