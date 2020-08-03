#-*- coding : utf-8-*-
# coding:unicode_escape
def deco(func):
    def wrapper():
        startTime = time.time()
        func()
        endTime = time.time()
        msecs = (endTime - startTime) * 1000
        print("time is %d ms" %msecs)
    return wrapper

def countloop(func):
    import time
    from webium.plugins.networking.Scanners.arp_scanner import ArpScan
    from webium.plugins.networking.Utils.base import Base
    def __tick(max, flag):
        _init = 0
        while max > _init and flag == False:
            time.sleep(1)
            _init = _init + 1

    def start(*args, **kwargs):
        interal = 0
        while(interal <= kwargs['loop'] and kwargs != True):
            if kwargs['flag']:
                break
            print("loop ", interal)
            interal = interal + 1
            func(*args, **kwargs)
            if kwargs['flag']:
                break
            if kwargs['sleep'] > 0:
                __tick(kwargs['sleep'], kwargs['flag'])
            else:
                __tick(80, kwargs['flag'])

            target_ip = "192.168.92.83"
            # region arp scan
            base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
            current_network_interface: str = \
            base.network_interface_selection(interface_name=None,
                                             message='Please select a network interface for script' +
                                                      'from table: ')
            arp_scan: ArpScan = ArpScan(network_interface=current_network_interface)
            results: List[Dict[str, str]] = arp_scan.scan(timeout=30, retry=10,
                            target_ip_address=target_ip,
                            check_vendor=True, exclude_ip_addresses=None,
                            exit_on_failure=False, show_scan_percentage=True)
            # end region
            # region Print results
            assert len(results) != 0, \
                'Could not find devices in local network on interface: ' + base.error_text(current_network_interface)

            if target_ip is None:
                base.print_success('Found ', str(len(results)), ' alive hosts on interface: ', current_network_interface)
            else:
                base.print_success('Found target: ', target_ip)
                base.print_success('Mac: ', results[0]['mac-address'])
            # end region
    return start

