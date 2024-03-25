# Routing

You may run the distancevector.py like so:
python .\distancevector.py .\topology.txt .\message.txt .\changes.txt

Since the linkstate part has some imported libraries that require pip installations, we have created a docker container for it.

To test our implementations, use the following commands inside the src folder:
docker build -t linkstate1 .
docker run linkstate1
docker run linkstate1
docker cp <docker contrainer ID>:/app/output.txt .\output.txt