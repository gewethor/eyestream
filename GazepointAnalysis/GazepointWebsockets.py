###############################################################################
# GazepointWebsockets: This project converts eye tracker data collected from a
# Gazepoint GP3 to simple JSON and then sends collected events to an
# experimentation platform, such as the Cybertrust phishing research platform,
# using websockets.
#
# Author: Matthew L. Hale
# Email: mlhale@unomaha.edu
# Copyright (C) 2017 Dr. Matthew L. Hale
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.
# Based on PyOpenGaze by Edwin Dalmaijer (edwin.dalmaijer@psy.ox.ac.uk)
###############################################################################
import json

from opengaze import OpenGazeTracker

class GazepointWebsockets(OpenGazeTracker):
    def __init__(self, api_user, socket, socketsend, ip='127.0.0.1', port=4242, logfile='default.tsv', debug=False, ):
        OpenGazeTracker.__init__(self, ip, port, logfile, debug)
        self._api_user = api_user
        self._socket = socket
        self._socketsend = socketsend

    # Accepts a sample as a list of keys and returns a JSON object
    def sampleToJSON(self, sample):
        # append apiuser variable
        sample['apiuser'] = self._api_user
        return json.dumps(sample, sort_keys=True, ensure_ascii=True,)

    # Method is invoked by a PyOpenGaze logging thread to process an incoming sample data point from the Gazepoint API
    # Overridden to convert to JSON and issue a corresponding API request
    def _log_sample(self, sample):
        json_sample = self.sampleToJSON(sample);
        try:
            # print 'Sending to socket'
            # print json_sample
            self._socketsend({'text':json_sample})
            # print '---------------------------------------------\n'
        except Exception as e:
            print e
