import numpy as np
import gnuplotlib as gp

###################################################
#           Fuzzy libary for python3
###################################################
# Written by Magnus Sörensen GitHub:byteofsoren
###################################################
# The fuzzy rule-based system created in this
# library is based on Ning Xiongs lecturs
#
# The thought is you have an input then the
# following:
# 1.Fuzzy fication
#   Compute the membership degrees of each input
#   to the system with respect to linguistic
#   terms.
# 2. Rule Matching:
#   Calculate the firing strength (degrees of
#   satification) of the induvidual rules.
# 3. Fuzzy Implication:
#   determine the suggestions of rules according
#   to firing strengths and rule conclusions
# 4. Fuzzy Aggregation:
#   combine suggestions from individual rules into
#   an overall output fuzzy set.
# 5. Defuzzification:determine a crisp value
#   from the output membership function
#   as the final result or solution.
#
###################################################


class fuzzy_member():
    """ The member is the part of a set"""
    def __init__(self):
        self.points = None
        self._shape = None
        self._linear= None
        self._fire = None
        pass

    def fire(x:float):
        """ Calculates the membership from the input
            Needs to be implemented in the sub class.

        """
        return 0

    def __rmul__(self,other):
        return self.__mul__(other)

    def __mul__(self,other):
        """ Multiplication is the rule AND funcion
            let:
                cold = fuzzy_member
                cheap = fuzzy_member
            then:
                A rule named R1 can be defiined as:
                R1 = cold*cheep
                R1(x) => min(cold.fire(x),cheep.fire(x))
        """
        if isinstance(other, fuzzy_member):
            return lambda : np.min([other._fire, self._fire])
        elif callable(other):
            return lambda : np.min([other(), self._fire])

    def __repr__(self):
        return lambda : self._fire

    def __radd__(self,other):
        return self.__add__(other)

    def __add__(self,other):
        """ Aaddition is the rule OR funcion
            let:
                cold = fuzzy_member
                cheap = fuzzy_member
            then:
                A rule named R1 can be defiined as:
                R1 = cold + cheep
                R1(x) => max(cold.fire(x),cheep.fire(x))
        """
        if isinstance(other, fuzzy_member):
            return lambda : np.max([other._fire, self._fire])
        elif callable(other):
            return lambda : np.max([other(), self._fire])

    def plot(self,terminal=True, xpad=[-1,1], ypad=[-0.2,1.2]):
        """ Plots the fuzzy_member to ether the terminal or gui
            terminal=True plots the fuzzy_member to terminal else gui.
            xpad = [-1,1] adds x padding to the plots so that it prints niser
            ypad = [-0.2, 1.2] adds y padding to the plot so it prints niser
            return None
        """
        x = np.arange(self.points[0,0]+xpad[0],self.points[-1,0]+xpad[1],0.01)
        y = np.array(list(map(lambda x: float(self.fire(x)[0]), x)))
        print(f'shapes x={np.shape(x)} y={np.shape(y)}')
        if terminal:
            gp.plot(x,y, _yrange = ypad, terminal="dumb 80,20", unset='grid')
        else:
            gp.plot(x,y, _yrange = ypad,  unset='grid')


class fuzzy_member_pointlist(fuzzy_member):
    """ Creates an fuzzy memmber using a point list such:
        member = fuzzy_member_pointlist([[1,0],[3,1],[5,1],[7,0]])
    """

    def __init__(self, points:list, filename:str=None, inf=[-10e10,10e10]):
        super(fuzzy_member_pointlist, self).__init__()
        self.points = np.array(points)
        self._shape = np.shape(self.points)
        if filename == None:
            # No file to load use the points list
            try:
                if (self._shape[0] == 2 or self._shape[1] == 2) and (np.min(self._shape) > 2):
                    # its a point list with [[x1,y1],[x2,y2]..] or [[x1, x2, x3],[y1,y2,y3]]
                    # Is transposed to the first version [[x1,y1],[x2,y2]...]
                    if self._shape[0] < self._shape[1]:
                        self.points = self.points.T

            except Exception as e:
                    raise ValueError('ERROR: wrong shape on list')
            # Adding points to infinity to the self.points
            self._pointinf = np.array([[inf[0], self.points[0,1]]])
            self._pointinf = np.vstack((self._pointinf, self.points))
            self._pointinf = np.vstack((self._pointinf, np.array((inf[0], self.points[-1,1]))))
            # Calculating the y=k*x + m for all lines
            A = np.vstack((self._pointinf[:,0],np.ones(len(self._pointinf)))).T
            km = None
            for index in np.arange(len(self._pointinf)-1):
                y = self._pointinf[index:index+2,1]
                params = np.linalg.lstsq(A[index:index+2,:],y,rcond=None)[0]
                # print(f'params={params}')
                if km is None:
                    km = np.array(params)
                else:
                    km = np.vstack((km, params))

            # print(km)
            # xlim = array of al first limits
            xlim = np.array([self._pointinf[:-1,0]])
            # xlim1 = array of limit xlim + 1
            xlim1 = np.roll(xlim,-1)
            # After rol the last limit in the list is -inf
            # Change that to inf
            xlim1[-1,-1] = inf[1]
            # print(f'xlim={xlim}')
            # print(f'xlim1={xlim1}')
            # [xlim, xlim+1, k, m]
            limconf = np.vstack((xlim[0], xlim1[0]))
            self._linear = np.vstack([limconf, km.T]).T

    def __str__(self):
        return f'Fuzzy member with the points:\n{self.points}'

    def fire(self, x:float):
        """ Fire test the membership for input x"""
        # Make a boolean selection matrix for a single True, Fals for each row
        select = np.logical_and(self._linear[:,0] < x, x <= self._linear[:,1])
        # Extend for all column on the row by:
        select = np.tile(select, (2,1)).T
        match = self._linear[:,2:4]
        # is now a [True,False] matrix with same dimentions as self._linear
        equations = match[select].T
        # The rows in selected are [xlim, xlim+1, k, m]
        X = np.array([[x,1]]).T
        # print(f'equations = \n{equations}\nX =\n {X}')
        # The linear equaiton can be calculated by [k,m]*[[x,1]].T => y=kx+m
        # However the [k,m] can be more then one row thus calculating the
        # Value for every line in that segment.
        self._fire = equations@X
        return self._fire






class fuzzy_rule():
    """Creat rules with the fuzzy_rule object"""
    def __init__(self, condition, statement:fuzzy_member):
        self.condition = condition
        self.statement = statement

    def min_implication(self, t):
        return t

    def prod_implication(self, t):
        return t




















