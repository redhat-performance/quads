import Connect

# Old ass SSH crap
options = {
            "KexAlgorithms": "+diffie-hellman-group1-sha1",
            "HostKeyAlgorithms": "+ssh-dss",
            "StrictHostKeyChecking": "no",
            "UserKnownHostsFile": "/dev/null"}

s = Connect.Connect("My Test Host","user","pass",options)
prompt="Switched CDU: "
if not s.special_login(prompt=prompt):
    print "Error logging in"
    exit(1)

outlets = s.execute("list outlets",["More",prompt])
print outlets[0]
while outlets[1] is 0 :
    outlets = s.execute("yes",["More",prompt])
    print outlets[0]
