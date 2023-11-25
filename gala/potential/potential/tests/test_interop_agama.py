"""
Test converting the builtin Potential classes to Agama
"""

# Third-party
import astropy.units as u
import numpy as np
import pytest

# This project
from gala.potential import LogarithmicPotential
from gala.tests.optional_deps import HAS_AGAMA
from gala.units import galactic

if HAS_AGAMA:
    from gala.potential.potential.interop import _gala_to_agama


def pytest_generate_tests(metafunc):
    # Some magic, semi-random numbers below!
    gala_pots = []
    other_pots = []

    if not HAS_AGAMA:
        return

    # Test the Gala -> Agama direction
    for Potential in _gala_to_agama.keys():
        init = {}
        len_scale = 1.0
        for k, par in Potential._parameters.items():
            if k == "m":
                val = 1.43e10 * u.Msun
            elif par.physical_type == "length":
                val = 5.12 * u.kpc * len_scale
                len_scale *= 0.5
            elif par.physical_type == "dimensionless":
                val = 1.0
            elif par.physical_type == "speed":
                val = 201.41 * u.km / u.s
            else:
                continue

            init[k] = val

        pot = Potential(**init, units=galactic)
        other_pot = pot.as_interop("agama")

        gala_pots.append(pot)
        other_pots.append(other_pot)

    # Make a composite potential too:
    gala_pots.append(gala_pots[0] + gala_pots[1])
    other_pots.append(gala_pots[-1].as_interop("agama"))

    test_names = [
        f"{g1.__class__.__name__}:{g2.__class__.__name__}"
        for g1, g2 in zip(gala_pots, other_pots)
    ]

    metafunc.parametrize(
        ["gala_pot", "other_pot"], list(zip(gala_pots, other_pots)), ids=test_names
    )


@pytest.mark.skipif(
    not HAS_AGAMA, reason="must have agama installed to run these tests"
)
class TestAgamaInterop:
    def setup_method(self):
        # Test points:
        rng = np.random.default_rng(42)
        ntest = 4

        xyz = rng.uniform(-25, 25, size=(3, ntest)) * u.kpc
        self.xyz = xyz.copy()

    def test_density(self, gala_pot, other_pot):
        gala_val = gala_pot.density(self.xyz).decompose(gala_pot.units).value
        other_val = other_pot.density(self.xyz.decompose(gala_pot.units).value.T)
        assert np.allclose(gala_val, other_val)

    def test_energy(self, gala_pot, other_pot):
        if isinstance(gala_pot, LogarithmicPotential):
            # TODO: Agama has an inconsistency with Gala's log potential energy
            pytest.skip()
        gala_val = gala_pot.energy(self.xyz).decompose(gala_pot.units).value
        other_val = other_pot.potential(self.xyz.decompose(gala_pot.units).value.T)
        assert np.allclose(gala_val, other_val)

    def test_acc(self, gala_pot, other_pot):
        gala_val = gala_pot.acceleration(self.xyz).decompose(gala_pot.units).value
        other_val = other_pot.force(self.xyz.decompose(gala_pot.units).value.T).T
        assert np.allclose(gala_val, other_val)

    # def test_vcirc(self, gala_pot, galpy_pot):
    #     tmp = self.xyz.copy()
    #     tmp[2] = 0.0

    #     if not hasattr(galpy_pot, "vcirc") or isinstance(
    #         gala_pot, gp.LongMuraliBarPotential
    #     ):
    #         pytest.skip()

    #     gala_vcirc = gala_pot.circular_velocity(tmp).to_value(u.km / u.s)
    #     galpy_vcirc = np.array([galpy_pot.vcirc(R=RR) for RR, *_ in self.Rpz_iter])
    #     assert np.allclose(gala_vcirc, galpy_vcirc)
