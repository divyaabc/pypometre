import itertools
import sys
import hashlib
import random
import subprocess
import time
import os
from pypometre_optparser import opt_parser_pypoblitz

try: 
    combinations = itertools.combinations
except: 
   def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices) 

def runProcess(args):
  f1, f2 = args
  #d = os.path.realpath('.')
  import time
  time.sleep(3)
  d = open('/etc/hostname').read()
  open(d, 'w').write(d)
  #pypometre.main(['', '-q', '-o', '/dev/null', f1, f2])
  return d

class RunningMethod:
    def __init__(self, args): 
        self._args = args
        self._commands = []

class RunningMethod_pp(RunningMethod):
    def __init__(self, args):
        RunningMethod.__init__(self, args)
        import pp
        ppservers=("*",)
        self._jobServer = pp.Server(ppservers=ppservers)

    def addCommand(self, f_out, f1, f2):
        cmd = ((f1, f2), f_out)
        self._commands.append(cmd) 

    def run(self):
        start_t = time.time()
        pid = -1
        maxCmds = len(self._commands)
        allJobs = []
        for nbCmds, cmd in enumerate(self._commands):
            nbcmds = nbCmds+1
#            print >>sys.stderr, "+ [t=%3.0f]    pid=%8d    idx=%4d/%4d "%(time.time()-start_t, pid, nbCmds, maxCmds)
#            t = time.time() 
            (f1, f2), f_out = cmd
            job = self._jobServer.submit(runProcess, ((f1,f2),)) 
            allJobs.append(job)       
            #subprocess.call(["/bin/sh", "-c", cmd])
#            print >>sys.stderr, "- [t=%3.0f]    pid=%8d    dur=%6.0fs"%(time.time()-start_t, pid, time

#        for job in allJobs:
#            print job()

class RunningMethod_list(RunningMethod):
    def addCommand(self, f_out, f1, f2):
        cmd = "python pypometre.py %s -q -o %s %s %s"%(self._args, f_out, f1, f2) 
        self._commands.append(cmd) 

    def run(self):
        start_t = time.time()
        pid = -1
        maxCmds = len(self._commands)
        for nbCmds, cmd in enumerate(self._commands):
            nbcmds += 1
#            print >>sys.stderr, "+ [t=%3.0f]    pid=%8d    idx=%4d/%4d "%(time.time()-start_t, pid, nbCmds, maxCmds)
            print >>sys.stderr, "idx=%4d/%4d "%(nbCmds, maxCmds)
#            t = time.time() 
            subprocess.call(["/bin/sh", "-c", cmd])
#            print >>sys.stderr, "- [t=%3.0f]    pid=%8d    dur=%6.0fs"%(time.time()-start_t, pid, time.time() - t)

class RunningMethod_qsub(RunningMethod):
    def addCommand(self, f_out, f1, f2):
        f1 = os.path.realpath(f1)
        f2 = os.path.realpath(f2)
        f_out = os.path.realpath(f_out)
        curdir = os.path.realpath('.')
        cmd = 'echo "python pypometre.py -q -o %s %s %s" | qsub -d %s'%(f_out, f1, f2, curdir) 
        self._commands.append(cmd) 

    def run(self):
        start_t = time.time()
        pid = -1
        maxCmds = len(self._commands)
        jobs = []
        for nbCmds, cmd in enumerate(self._commands):
            nbcmds = nbCmds+1
            print >>sys.stderr, "+ [t=%3.0f]    pid=%8d    idx=%4d/%4d "%(time.time()-start_t, pid, nbCmds, maxCmds)
            t = time.time() 
            subprocess.call(["/bin/sh", "-c", cmd])
            print >>sys.stderr, "- [t=%3.0f]    pid=%8d    dur=%6.0fs"%(time.time()-start_t, pid, time.time() - t)

class RunningMethod_fork(RunningMethod):

    def addCommand(self, f_out, f1, f2):
        cmd = "python pypometre.py -q -o %s %s %s"%(f_out, f1, f2)
        self._commands.append(cmd) 

    def run(self):
        maxProcesses = 4
        
        nbProcesses = 0
        processes = {}
        allCmds = self._commands
        cmds = iter(allCmds)
        nbCmds = 0
        maxCmds = len(allCmds)

        start_t = time.time()
        while 1:
            if nbProcesses < maxProcesses:
                try:
                  currentCmd = allCmds[nbCmds]
                  args = currentCmd.split()
                  pid = os.fork()
                  if pid == 0:
                    os.execlp(args[0], *args)
                  else:
                    nbCmds += 1
#                    print >>sys.stderr, "+ [t=%3.0f]    pid=%8d    idx=%4d/%4d "%(time.time()-start_t, pid, nbCmds, maxCmds)
                    print >>sys.stderr, "+ %4d/%4d "%(nbCmds, maxCmds)
#                    print >>sys.stderr, "    %s"%(currentCmd)
                    processes[pid] = (currentCmd, time.time())
                    nbProcesses += 1
                except IndexError, e:
                    pass
            pid, res = os.waitpid(0, os.WNOHANG)
            if pid > 0:
              cmd, t = processes[pid]
#              print >>sys.stderr, "- [t=%3.0f]    pid=%8d    dur=%6.0fs"%(time.time()-start_t, pid, time.time() - t)
              #print >>sys.stderr, "    %s"%(cmd)
              nbProcesses -= 1
              if nbProcesses == 0:
                if nbCmds >= len(allCmds):
                    break
            time.sleep(0.1)

def getFileContent(f):
    while 1:
        try:
            data = eval(open(f).read())
            return data
        except Exception, e:
            time.sleep(0.1)

def fusion_js(lst_f_out, out) :
    corpus = set()
    scores = {}
    for f_out in lst_f_out:
      data = getFileContent(f_out)
      signature = data['signature']
      f1, f2 = data['filenames'] 
      corpus.add(f1)
      corpus.add(f2)
      f1_x_f2 = data['corpus_scores']
      scores[(f1, f2)] = f1_x_f2[0][1]
      scores[(f2, f1)] = f1_x_f2[1][0]

    corpus = list(corpus)
    documents_distances = [[0 for _ in corpus] for _ in corpus]
    for i1, f1 in enumerate(corpus):
      for i2, f2 in enumerate(corpus):
        documents_distances[i1][i2] = scores.get((f1, f2), 0.0)

    print_json = '{"signature" : \'{}\',\n "filenames" : \n  '
    list_str_document = [str(document) for document in corpus]
    print_json += '%s ,\n "corpus_scores" : \n  %s \n}'%(str(list_str_document),str(documents_distances))
    file_out = open("%s.js"%out,'w')
    file_out.write(print_json)
    file_out.close()

def main(args=sys.argv[1:]):
  parser = opt_parser_pypoblitz()
  (opt_options, opt_args) = parser.parse_args(args)
  out = opt_options.fileout
  files = opt_args
  
  Method = eval("RunningMethod_" + opt_options.method)
  method = Method(opt_options.args)

  lst_f_out = []

  t0 = time.time()
  try:
    os.mkdir(out)
  except:
    pass
  for d1, d2 in combinations(files, 2):
    f_out = "%s/out_%s.js"%(out, hashlib.md5("%s"%random.random()).hexdigest())
    lst_f_out.append(f_out)
    method.addCommand(f_out, d1, d2)
  method.run()
  
  fusion_js(lst_f_out, out)
  print "Total duration :", time.time() - t0
    
main()    
