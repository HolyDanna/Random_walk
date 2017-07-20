import LRRandom

# 0 is for bottom
# 1 is for left
# 2 is for top
# 3 is for right
# these values were chosen to make some calculations easier
# Bottom top is + for x/y values
# the "path" is stored as an int
# writing said int in base 3 will reveal the path, using the direction given above
# the number of steps allows us to know how many steps towards the top there
# were at the beginning

class walker(object):
    def __init__(self, type="C"):
        super(walker, self).__init__()
        self.path = 0
        self.dir = 0
        self.x = 0
        self.y = 0
        self.steps = 0
        # this will be used for the self-avoiding possibilities
        self.failures = []
        self.type = type
        self.RNG = LRRandom.LRR(x1=19784, x2=475467)
        self.counter=0

    # reset the values, without resetting the RNG
    def reset(self):
        self.path=0
        self.dir=0
        self.x = 0
        self.y = 0
        self.steps = 0
        self.counter=0
        self.failures = []

    # change the type using the value given by the Radiobutton
    def setType(self,stype):
        if stype == 0:
            self.type = "C"
        elif stype == 1:
            self.type = "S"
        elif stype == 2:
            self.type = "U"
        else:
            self.type = "C"


    # this fonction is called when we get blocked during a self-avoiding path
    def correct_error(self):
        self.counter+=1
        # we add the current path to the "failure" paths
        self.failures.append(self.path)
        # we get last direction
        last_dir = self.path%4
        # we move back where we were
        if last_dir%2:
            self.x -= last_dir - 2
        else:
            self.y -= last_dir - 1
        # we correct the path
        self.path = self.path//4
        self.steps -= 1


    # allows you to get the list of neighboring tiles where you still
    # haven't gone to, for the 3rd possibility
    def available_tiles(self):
        # the 4 neighboring tiles
        pos_tiles = [[self.x,self.y-1],[self.x-1,self.y],
                    [self.x,self.y+1],[self.x+1,self.y]]
        pos_dir = [0,1,2,3]
        j=0
        # we remove all elements that lead to "failures"
        for k in range(4):
            if 4*self.path+k in self.failures:
                pos_tiles.pop(j)
                pos_dir.pop(j)
                j = j - 1
            j = j + 1
        # the cur_ variables represent the position already moved through during
        # updates
        cur_x = 0
        cur_y = 0
        cur_dir = 0

        # this one takes care of the position (0,0), which is not considered otherwise
        if [cur_x,cur_y] in pos_tiles:
            index = pos_tiles.index([cur_x,cur_y])
            pos_tiles.remove([cur_x,cur_y])
            pos_dir.pop(index)

        # we loop on the steps we got through
        for i in reversed(range(self.steps)):
            cur_dir = (self.path//4**i)%4
            if cur_dir%2:
                # the direction is either 1 (left) or 3 (right)
                # We then get -1 or 1, by substracting 2
                cur_x += cur_dir - 2
            else:
                # same logic as above
                cur_y += cur_dir - 1
            # if the case we're could be accessed at next step, we remove it from
            # the list
            if [cur_x,cur_y] in pos_tiles:
                index = pos_tiles.index([cur_x,cur_y])
                pos_tiles.remove([cur_x,cur_y])
                pos_dir.pop(index)

        # We only got neighboring tiles we did not yet stop on, now.
        # the directions corresponding to said tiles are in pos_dir
        # we return these directions
        return pos_dir

    # update the walker
    # he will try to continue forward, but will move back if he can't advance anymore
    # when doing self-avoidance
    def update(self):
        # for 1st case, we just take a random possibility for the 4
        if self.type=="C":
            self.dir = (self.dir + self.RNG.randint(4)) % 4
        # for the 2nd case, we take a random possibility out of the 3 possible
        # we just need some maths to make sure we don't get back on our tracks
        elif self.type=="S":
            self.dir = (self.dir - 1 + self.RNG.randint(3)) % 4
        elif self.type=="U":
            pos_dir = self.available_tiles()
            if len(pos_dir):
                self.dir = pos_dir[self.RNG.randint(len(pos_dir))]
            else:
                self.correct_error()
                return -1

        self.path = 4*self.path + self.dir
        self.steps+=1
        if self.dir%2:
            self.x += self.dir - 2
        else:
            self.y += self.dir - 1
        return self.dir

    def getPath(self):
        return self.path

    def getStepNbr(self):
        return self.steps
