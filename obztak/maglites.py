#!/usr/bin/env python
"""
Code related to the Magellanic Satellites Survey (MagLiteS).
"""
import os,sys
import logging
import copy

import numpy as np

from obztak.field import FieldArray, SISPI_DICT, SEP
from obztak.survey import Survey

from obztak.utils import constants
from obztak.utils.constants import BANDS,SMASH_POLE,CCD_X,CCD_Y,STANDARDS
from obztak.utils.projector import cel2gal, angsep
from obztak.utils.date import datestring
from obztak.utils import fileio

NAME = 'MagLiteS'
PROGRAM = NAME.lower()
PROPID  = '2016A-0366'

class MagLiteS(Survey):
    """ Survey sublcass for MagLiteS. """

    """
    # One season prediction
    nights = [['2016/2/10', 'second'],
              ['2016/2/11', 'second'],
              ['2016/2/12', 'second'],
              ['2016/2/13', 'second'],
              ['2016/2/14', 'second'],
              ['2016/2/15', 'second'],
              ['2016/6/27', 'full'],
              ['2016/6/28', 'full'],
              ['2016/6/29', 'full']]
    """
    """
    # Two seasons prediction
    nights = [['2016/2/10', 'second'],
              ['2016/2/11', 'second'],
              ['2016/2/12', 'second'],
              ['2016/2/13', 'second'],
              ['2016/2/14', 'second'],
              ['2016/2/15', 'second'],
              ['2016/6/27', 'full'],
              ['2016/6/28', 'full'],
              ['2016/6/29', 'full'],
              ['2017/2/18', 'second'],
              ['2017/2/19', 'second'],
              ['2017/2/20', 'second'],
              ['2017/2/21', 'second'],
              ['2017/2/22', 'second'],
              ['2017/2/23', 'second'],
              ['2017/6/27', 'full'],
              ['2017/6/28', 'full'],
              ['2017/6/29', 'full']]
    """

    """
    In 2017A, we are considering a few different possible observing periods.

    Early run (choose one)
    * 2017/2/01
    * 2017/3/02

    + Late run (choose one)
    * 2017/6/17
    * 2017/7/16
    """
    """
    # 2017A prediction (feb1jun17)
    nights = [['2017/2/01', 'second'],
              ['2017/2/02', 'second'],
              ['2017/2/03', 'second'],
              ['2017/2/04', 'second'],
              ['2017/2/05', 'second'],
              ['2017/2/06', 'second'],
              ['2017/6/17', 'full'],
              ['2017/6/18', 'full'],
              ['2017/6/19', 'full']]

    # 2017A prediction (feb1jul16)
    nights = [['2017/2/01', 'second'],
              ['2017/2/02', 'second'],
              ['2017/2/03', 'second'],
              ['2017/2/04', 'second'],
              ['2017/2/05', 'second'],
              ['2017/2/06', 'second'],
              ['2017/7/16', 'full'],
              ['2017/7/17', 'full'],
              ['2017/7/18', 'full']]

    # 2017A prediction (mar2jun17)
    nights = [['2017/3/02', 'second'],
              ['2017/3/03', 'second'],
              ['2017/3/04', 'second'],
              ['2017/3/05', 'second'],
              ['2017/3/06', 'second'],
              ['2017/3/07', 'second'],
              ['2017/6/17', 'full'],
              ['2017/6/18', 'full'],
              ['2017/6/19', 'full']]
    """
    """
    # 2017A prediction (mar2jul16)
    nights = [['2017/3/02', 'second'],
              ['2017/3/03', 'second'],
              ['2017/3/04', 'second'],
              ['2017/3/05', 'second'],
              ['2017/3/06', 'second'],
              ['2017/3/07', 'second'],
              ['2017/7/16', 'full'],
              ['2017/7/17', 'full'],
              ['2017/7/18', 'full']]
    """

    # 2017A prediction (Moon up during second half of night)
    #nights = [['2017/2/18', 'second'],
    #          ['2017/2/19', 'second'],
    #          ['2017/2/20', 'second'],
    #          ['2017/2/21', 'second'],
    #          ['2017/2/22', 'second'],
    #          ['2017/2/23', 'second'],
    #          ['2017/6/17', 'full'],
    #          ['2017/6/18', 'full'],
    #          ['2017/6/19', 'full']]

    # 2017A ACTUAL
    nights = [['2017/2/21', 'full'],
              ['2017/2/22', 'full'],
              ['2017/2/23', 'full'],
              ['2017/6/18', 'full'],
              ['2017/6/19', 'full'],
              ['2017/6/20', 'full']]

    def prepare_fields(self, infile=None, outfile=None, mode='smash_dither', plot=True, smcnod=False):
        """ Create the list of fields to be targeted by this survey.

        Parameters:
        -----------
        infile : File containing all possible field locations.
        outfile: Output file of selected fields
        mode   : Mode for dithering: 'smash_dither', 'smash_rotate', 'decam_dither', 'none'
        plot   : Create an output plot of selected fields.

        Returns:
        --------
        fields : A FieldArray of the selected fields.
        """
        # Import the dither function here...
        #def dither(ra,dec,dx,dy):
        #    return ra,dec

        if mode is None or mode.lower() == 'none':
            def dither(ra,dec,dx,dy):
                return ra,dec
            TILINGS = [(0,0),(0,0),(0,0),(0,0)]
        elif mode.lower() == 'smash_dither':
            TILINGS = [(0,0), (1.0,0.0), (-1.0,0.0), (0.0,-0.75)]
            dither = self.smash_dither
        elif mode.lower() == 'smash_rotate':
            TILINGS = [(0,0), (0.75,0.75), (-0.75,0.75), (0.0,-0.75)]
            dither = self.smash_rotate
        elif mode.lower() == 'decam_dither':
            TILINGS = [(0., 0.),(8/3.*CCD_X, -11/3.*CCD_Y),
                       (8/3.*CCD_X, 8/3.*CCD_Y),(-8/3.*CCD_X, 0.)]
            dither = self.decam_dither

        if infile is None:
            infile = os.path.join(fileio.get_datadir(),'smash_fields_alltiles.txt')
        data = np.recfromtxt(infile, names=True)

        # Apply footprint selection after tiling/dither
        #sel = obztak.utils.projector.footprint(data['RA'],data['DEC'])

        # This is currently a non-op
        smash_id = data['ID']
        ra       = data['RA']
        dec      = data['DEC']

        nhexes = len(data)
        #ntilings = len(DECAM_DITHERS)
        ntilings = len(TILINGS)
        nbands = len(BANDS)
        nfields = nhexes*nbands*ntilings

        logging.info("Number of hexes: %d"%nhexes)
        logging.info("Number of tilings: %d"%ntilings)
        logging.info("Number of filters: %d"%nbands)

        fields = FieldArray(nfields)
        fields['HEX'] = np.tile(np.repeat(smash_id,nbands),ntilings)
        fields['PRIORITY'].fill(1)
        fields['TILING'] = np.repeat(np.arange(1,ntilings+1),nhexes*nbands)
        fields['FILTER'] = np.tile(BANDS,nhexes*ntilings)

        #for i in range(ntilings):
        for i,tiling in enumerate(TILINGS):
            idx0 = i*nhexes*nbands
            idx1 = idx0+nhexes*nbands
            ra_dither,dec_dither = dither(ra,dec,tiling[0],tiling[1])
            fields['RA'][idx0:idx1] = np.repeat(ra_dither,nbands)
            fields['DEC'][idx0:idx1] = np.repeat(dec_dither,nbands)

        # Apply footprint selection after tiling/dither
        sel = self.footprint(fields['RA'],fields['DEC']) # NORMAL OPERATION
        if smcnod:
            # Include SMC northern overdensity fields
            sel_smcnod = self.footprintSMCNOD(fields) # SMCNOD OPERATION
            sel = sel | sel_smcnod
            #sel = sel_smcnod
            fields['PRIORITY'][sel_smcnod] = 99
        #if True:
        #    # Include 'bridge' region between Magellanic Clouds
        #    sel_bridge = self.footprintBridge(fields['RA'],fields['DEC'])
        #    sel = sel | sel_bridge
        sel = sel & (fields['DEC'] > constants.SOUTHERN_REACH)
        fields = fields[sel]

        logging.info("Number of target fields: %d"%len(fields))

        if plot:
            import pylab as plt
            import obztak.utils.ortho

            plt.ion()

            fig, basemap = obztak.utils.ortho.makePlot('2016/2/11 03:00',center=(0,-90),airmass=False,moon=False)

            proj = obztak.utils.ortho.safeProj(basemap,fields['RA'],fields['DEC'])
            basemap.scatter(*proj, c=fields['TILING'], edgecolor='none', s=50, cmap='Spectral',vmin=0,vmax=len(TILINGS))
            colorbar = plt.colorbar(label='Tiling')

            if outfile:
                outfig = os.path.splitext(outfile)[0]+'.png'
                fig.savefig(outfig,bbox_inches='tight')
            if not sys.flags.interactive:
                plt.show(block=True)

        if outfile: fields.write(outfile)

        return fields

    @staticmethod
    def footprint(ra,dec):
        l, b = cel2gal(ra, dec)

        angsep_lmc = angsep(constants.RA_LMC, constants.DEC_LMC, ra, dec)
        angsep_smc = angsep(constants.RA_SMC, constants.DEC_SMC, ra, dec)
        sel = (np.fabs(b) > 10.) \
              & ((angsep_lmc < 30.) | (angsep_smc < 30.)) \
              & (dec < -55.) & (ra > 100.) & (ra < 300.)
        #sel = sel | ((dec < -65.) & (angsep_lmc > 5.) & (angsep_smc > 5.))
        sel = sel | ((dec < -65.) & (ra > 300.) & (ra < 360.)) # SMC
        sel = sel | (dec < -80.)

        return sel

    @staticmethod
    def footprintSMCNOD(fields):
        """
        Special selection for pointings near the SMC Northern Overdensity (SMCNOD)
        """
        sel = np.in1d(fields['HEX'], constants.HEX_SMCNOD) \
              & np.in1d(fields['TILING'], constants.TILING_SMCNOD)
        return sel

    @staticmethod
    def footprintBridge(ra, dec):
        """
        Special selection for pointings near the SMC Northern Overdensity (SMCNOD)
        """
        sel = (ra > 30.) & (ra < 60.) & (dec < -65.)
        return sel

class MagLiteSFieldArray(FieldArray):
    SISPI_DICT = copy.deepcopy(SISPI_DICT)
    SISPI_DICT["program"] = PROGRAM
    SISPI_DICT["propid"] = PROPID

    OBJECT_FMT = NAME.upper() + ' field'+SEP+' %s'
    SEQID_FMT  = NAME.upper() + ' scheduled'+SEP+' %(DATE)s'


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()