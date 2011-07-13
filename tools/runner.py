import sys, os
import time

fileName = sys.argv[1]
maxProcesses = int(sys.argv[2])
nbProcesses = 0

processes = {}

allCmds = [cmd.strip() for cmd in open(fileName).readlines()]
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
            print >>sys.stderr, "+ [t=%6.0f]    pid=%8d    idx=%4d/%4d "%(time.time()-start_t, pid, nbCmds, maxCmds)
            print >>sys.stderr, "    %s"%(currentCmd)
            processes[pid] = (currentCmd, time.time())
            nbProcesses += 1    
        except IndexError:
            pass
    pid, res = os.waitpid(0, os.WNOHANG)
    if pid > 0:  
      cmd, t = processes[pid]
      print >>sys.stderr, "- [t=%6.0f]    pid=%8d    dur=%6.0fs"%(time.time()-start_t, pid, time.time() - t)
      print >>sys.stderr, "    %s"%(cmd)
      nbProcesses -= 1
      if nbProcesses == 0:
        if nbCmds >= len(allCmds):
            break

    time.sleep(0.01)

