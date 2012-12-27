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

from traits.api import HasTraits, Int, Float, Property
from traitsui.api import View, Item


class MicropointAttenuator(HasTraits):
    division = Int(1)
    # FIXME: `percent_transmission' should not be a Property.  There
    # should be a way for the user to change `percent_transmission'
    # and have `division change' in response, but perhaps this
    # circular dependency resolution is not trivial.
    percent_transmission = Property(Float, depends_on=['division'])
    # magnitude = Property(Float, depends_on=['division'])

    def attenuations(self, type="linear",
                     divisions=90, min_magnitude=0, max_magnitude=3):
        '''Returns array of transmission values for the mirror
        attenuator specifications.

        type must be set to "log" or "linear".

        We are assuming the linspace is perfectly logarithmic.  TODO:
        It would be nice to create a new function,
        "estimated_empirical_attenuation()" which uses sampled data to
        populate additional Trait Properties.'''
        log_attn = linspace(min_magnitude, max_magnitude, divisions)
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

    # FIXME: Add boundary conditions 1 <= division <= 90
    # TODO: Make `division' into a slider
    view = View(
        Item('division', label='Division'),
        Item('percent_transmission', label='Transmission %')
        )

mp = MicropointAttenuator()
mp.configure_traits()
