#!/usr/bin/env python
"""
Module for running survey operations.
"""
from datetime import datetime
import logging

import numpy as np
import ephem

from maglites.sim import Simulator
from maglites.utils import Database, datestring
import maglites.utils.constants as constants

import json

class Observer(Simulator):

    def __init__(self, infile_target_fields):
        super(Observer,self).__init__(infile_target_fields)
        self.accomplished_fields = self.getObservedFields()

        
    def run(self, tstart=None, tstop=None, plot=True):
        # If no tstop, run for 90 minutes
        timedelta = 90*ephem.minute
        if tstart is None: tstart = ephem.now()
        if tstop is None: tstop = tstart + timedelta

        # Convert strings into dates
        if isinstance(tstart,basestring):
            tstart = ephem.Date(tstart)
        if isinstance(tstop,basestring):
            tstop = ephem.Date(tstop)

        date = tstart
        latch = True
        while latch:
            # Check to see if in valid observation window
            if self.observation_windows is not None:
                inside = False
                for window in self.observation_windows:
                    if date >= window[0] and date <= window[-1]: 
                        inside = True 

                if not inside:
                    msg = 'Date is outside  nominal observing window: %s'%datestring(date)
                    logging.warning(msg)

            if date > tstop: latch = False

            if plot:
                print '  %s'%(datestring(date)),
            else:
                print '  %s'%(datestring(date))
            
            # Check 
            compute_slew = True
            if len(self.accomplished_fields['ID']) == 0:
                compute_slew = False
            else:
                if (date - ephem.Date(self.accomplished_fields['DATE'][-1])) > (30. * ephem.minute):
                    compute_slew = False
            if compute_slew:
                field_select = self.selectField(date, ra_previous=self.accomplished_fields['RA'][-1], dec_previous=self.accomplished_fields['DEC'][-1], plot=plot)
            else:
                field_select = self.selectField(date, plot=plot)
                
            id_select = field_select['ID']

            date = date + constants.FIELDTIME
            self.accomplished_field_ids.append(id_select)

            for key in field_select.keys():
                self.accomplished_fields[key].append(field_select[key])
                #if key not in self.accomplished_fields.keys():
                #    self.accomplished_fields[key] = [field_select[key]]
                #else:
                #    self.accomplished_fields[key].append(field_select[key])

        print len(self.accomplished_field_ids)

        # Clean up
        self.accomplished_field_ids = []

    def getObservedFields(self):
        """
        Get the fields that have been observed from the telemetry DB.
        """
        defaults = dict(propid = '2016A-0366', limit = '',dbname='db-fnal')
        
        params = dict(defaults)
        #if opts is not None: params.update(vars(opts))
        
        db = Database()
        db.connect()

        query ="""
        select object as ID, telra as RA, teldec as DEC, 
        1 as TILING, 1 as PRIORITY, utc_beg AS DATE, 
        COALESCE(airmass,-1) as AIRMASS, COALESCE(moonangl,-1) as MOONANGLE, 
        COALESCE(ha,-1) as HOURANGLE, COALESCE(slewangl,-1) as SLEW 
        from exposure where propid = '%(propid)s' %(limit)s
        """%params

        data = db.execute(query)
        names = map(str.upper,db.get_columns())

        if len(data): ret = np.rec.array(data,names=names)
        else:         ret = np.rec.recarray(0,names=names)

    @classmethod
    def write_json_script(self):
        pass


def main():
    tstart = '2016/2/11 05:20:28'
    tstop = '2016/2/11 06:20:28'
    fields = 'target_fields.txt'
    windows = 'observation_windows.txt'
    obs = Observer(fields)
    obs.loadObservationWindows(windows)
    obs.saveAccomplishedFields('accomplished_fields.txt')
    obs.run(tstart,tstop,plot=True)
    obs.saveAccomplishedFields('accomplished_fields_2.txt')

if __name__ == "__main__":
    import argparse
    description = __doc__
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()
    
    main()
    
