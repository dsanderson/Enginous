import SQLite, math, random

class Engenious():
    def __init__(db_location = None, keys = None, dist_func = None):
        #TODO db import/export
        self.keys = set(keys)
        self.dist_func = dist_func
        self.landmarks = {}

    def estimate_coverage(self, verbose = True):
        """use bootstrapping to estimate performance of current landmark set"""
        #TODO proper bootstrap calculations
        np = len(self.keys)
        #remove landmarks from potential candidates
        candidates = self.keys.difference(set(self.landmarks.keys()))
        nc = min(len(candidates),100)
        test_keys = random.choice(candidates, nc)
        df = lambda l,k: landmarks[l][k] #helper function for fast filtering while bootstrapping
        lens = []
        for key in test_keys:
            filtered_keys, l = filter_keys(self,self.landmarks,key,keys.remove(key),df)
            lens.append(len(filtered_keys))
        #from the list of numbers of points removed, calculate the average amount removed, and std.dev
        #first convert lengths to a percentage of points removed
        m = mean(lens)
        std = pstdev(lens)
        if verbose:
            print "Ran {} of {} points, removed {}% (standard deviation {})".format(nc,np,m*100,std*100)
        return m, std

    def filter_keys(self, landmarks, target, keys, dist_func=None):
        """removes keys that fall too far away from the target to be viable
        also returns the landmark closest to the target"""
        if dist_func == None:
            dist_func = self.dist_func
        closest_landmark = None
        for landmark in landmarks.keys():
            d = dist_func(landmark,key)
            if closest_landmark == None:
                closest_landmark = landmark
                closest = d
            elif closest > d:
                closest_landmark = landmark
                closest = d
            for key in list(keys):
                if d>2*landmarks[landmark][key]:
                    keys.remove(key)
        return keys, closest_landmark

    def add_landmark(self, key):
        self.landmarks[key] = {}
        for k in self.keys():
            if k!=key:
                self.landmarks[key][k] = self.dist_func(key,k)

    def search(self, target, threshold = 0.0):
        keys, closest_landmark = filter_keys(self,self.landmarks,target,self.keys)
        #search_order = self.landmarks[closest_landmark]
        closest = None
        for k in keys:
            d = self.dist_func(k,target)
            if closest == None:
                closest = k
                closest_dist = d
            elif d < closest_dist:
                closest = k
                closest_dist = d
        return closest, closest_dist

    def mean(data):
        """Return the sample arithmetic mean of data."""
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        return sum(data)/float(n) # in Python 2 use sum(data)/float(n)

    def _ss(data):
        """Return sum of square deviations of sequence data."""
        c = mean(data)
        ss = sum((x-c)**2 for x in data)
        return ss

    def pstdev(data):
        """Calculates the population standard deviation."""
        n = len(data)
        if n < 2:
            raise ValueError('variance requires at least two data points')
        ss = _ss(data)
        pvar = ss/n # the population variance
        return pvar**0.5
