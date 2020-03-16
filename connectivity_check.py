from pyats import aetest

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def check_topology(self,
                       testbed,
                       R1 = 'R1',
                       R2 = 'R2'):
        R1 = testbed.devices[R1]
        R2 = testbed.devices[R2]

        # add them to testscript parameters
        self.parent.parameters.update(ios1 = R1, R2 = R2)

        # get corresponding links
        links = R1.find_links(R2)

        assert len(links) >= 1, 'require one link between R1 and R2'


    @aetest.subsection
    def establish_connections(self, steps, ios1, ios2):
        with steps.start('Connecting to %s' % ios1.name):
            ios1.connect()

        with steps.start('Connecting to %s' % ios1.name):
            ios2.connect()

@aetest.loop(device = ('ios1', 'ios2'))
class PingTestcase(aetest.Testcase):

    @aetest.test.loop(destination = ('10.10.10.1', '10.10.10.2'))
    def ping(self, device, destination):
        try:
            result = self.parameters[device].ping(destination)

        except Exception as e:
            self.failed('Ping {} from device {} failed with error: {}'.format(
                                destination,
                                device,
                                str(e),
                            ),
                        goto = ['exit'])
        else:
            match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
            success_rate = match.group('rate')

            logger.info('Ping {} with success rate of {}%'.format(
                                        destination,
                                        success_rate,
                                    )
                               )

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, steps, ios1, ios2):
        with steps.start('Disconnecting from %s' % ios1.name):
            ios1.disconnect()

        with steps.start('Disconnecting from %s' % ios2.name):
            ios2.disconnect()

if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))