'''
Andor MicroPoint motorized attenuator power conversion utility.

Help support different software applications by converting between:
- 90 divisions of attenuation slider (non-linear).
- % transmission value (linear).
Also displays the power order of magnitude.
'''

__author__ = "Pariksheet Nanda"
__email__ = "p.nanda@andor.com"


from numpy import linspace, log10

from traits.api import HasTraits, Range, Float, Property
from traitsui.api import View, Item


class MicropointAttenuator(HasTraits):
    def __init__(self, divisions=90, min_magnitude=0,
                 max_magnitude=3, **traits):
        HasTraits.__init__(self, **traits)
        self.add_trait('division',
                       Range(low=1, high=divisions, value=1))
        self.divisions = divisions
        self.min_magnitude = min_magnitude
        self.max_magnitude = max_magnitude
    
    # FIXME: `percent_transmission' should not be a Property.  There
    # should be a way for the user to change `percent_transmission'
    # and have `division change' in response, but perhaps this
    # circular dependency resolution is not trivial.
    percent_transmission = Property(Float, depends_on=['division'])
    # magnitude = Property(Float, depends_on=['division'])
    
    def attenuations(self, type="linear"):
        '''Returns array of transmission values for the mirror
        attenuator specifications.

        type must be set to "log" or "linear".

        We are assuming the linspace is perfectly logarithmic.
        '''
        log_attn = linspace(self.min_magnitude,
                            self.max_magnitude,
                            self.divisions)
        if (type == "log"):
            return log_attn
        lin_attn = 10 ** log_attn
        if (type == "linear"):
            return lin_attn

    def _get_percent_transmission(self):
        attn_array = self.attenuations()
        perc_attn_array = (attn_array / attn_array.max()) * 100
        return perc_attn_array[self.division - 1]

    # def _get_magnitude

    view = View(
        Item('division', label='Division'),
        Item('percent_transmission', label='Transmission %')
        )

# If you want to simulate a manual attenuator, you could initialize
# something like:
#
# mp = MicropointAttenuator(divisions=30)
#
# TODO: It would be nice to have a radio button in the UI to toggle
# between manual and motorized presets.
mp = MicropointAttenuator()
mp.configure_traits()
