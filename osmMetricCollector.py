from osmclient import client
from osmclient.common.exceptions import ClientException
import yaml
from prettytable import PrettyTable


class OsmMetricCollector():
    def __init__(self,hostname="127.0.0.1", user="admin", password="admin", project="admin"):
        kwargs = {}
        if user is not None:
            kwargs['user'] = user
        if password is not None:
            kwargs['password'] = password
        if project is not None:
            kwargs['project'] = project
        self._osmclient = client.Client(host=hostname, sol005=True, **kwargs)
        self._nsi=self._osmclient.nsi
        self._ns=self._osmclient.ns
        self._vnf=self._osmclient.vnf

    def getNsiData(self):
        status=[]
        nsi=self._nsi
        if nsi is not None:
            currentNsi=nsi.list()[-1]
            #if currentNsi["config-status"]=="configured" and currentNsi["operational-status"]=="running":
            ops=nsi.list_op(currentNsi["id"])
            if ops is not None:
                for i in ops:
                    operation=nsi.get_op(i["id"])
                    c=[currentNsi["id"],operation["lcmOperationType"],operation["startTime"],operation["statusEnteredTime"]]
                    status.append(c)
                return currentNsi["nsr-ref-list"],status
            else:
                return
        else:
            return
        return nsi

    def getNsData(self, nsr=None):
        if nsr is None:
            return
        status = []
        ns = self._ns
        if ns is not None:
            availableNs=ns.list()
            availableNsId = [x["id"] for x in ns.list()]
            for currentNsr in nsr:
                if currentNsr["nsr-ref"] in availableNsId:
                    for i in availableNs:
                        if (i["id"] == currentNsr["nsr-ref"]):
                            currentNs=i

                    #if currentNs["config-status"] == "configured" and currentNs["operational-status"] == "running":
                    ops = ns.list_op(currentNs["id"])
                    if ops is not None:
                        for i in ops:
                            operation = ns.get_op(i["id"])
                            c = [currentNs["id"], operation["lcmOperationType"], operation["startTime"],
                                 operation["statusEnteredTime"]]
                            status.append(c)
                        return status
        return ns

    def getVnf(self):
        return


if __name__ == '__main__':
    metricCollector = OsmMetricCollector(hostname="10.0.12.216", user="admin", password="admin", project="admin")
    nsr_list,status_nsi=metricCollector.getNsiData()
    #nsr_ex=[{"nsr-ref":"ef33a536-65c4-48eb-bab1-9cdbdbe6d24a"}]
    status_ns=metricCollector.getNsData(nsr_list)
    final_status=[]
    status_nsi.insert(0,"OSM")
    final_status.append(status_nsi)
    for x in status_ns:
        x.insert(0,"OSM")
        final_status.append(x)

    print(final_status)
