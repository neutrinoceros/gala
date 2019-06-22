# Standard library
import warnings

# Third-party
import numpy as np

# Project
from ...integrate import DOPRI853Integrator
from .. import PhaseSpacePosition
from .df import StreaklineStreamDF, FardalStreamDF
from .mockstream_generator import MockStreamGenerator

__all__ = ['MockStream',
           'mock_stream', 'streakline_stream', # DEPRECATED: TODO remove
           'fardal_stream', 'dissolved_fardal_stream']

_transition_guide_url = "TODO"


class MockStream(PhaseSpacePosition):

    def __init__(self, pos, vel=None, frame=None, release_time=None):
        # TODO: a phase-space position that also knows about release times,
        # can separate particles by leading/trailing
        pass


# ---------------------------------------------------------------------------
# DEPRECATED / OLD STUFF BELOW
# TODO: remove this

def mock_stream(hamiltonian, prog_orbit, prog_mass, k_mean, k_disp,
                release_every=1, Integrator=DOPRI853Integrator,
                Integrator_kwargs=dict(),
                snapshot_filename=None, output_every=1, seed=None):
    """DEPRECATED!"""
    raise NotImplementedError(
        "This function has been deprecated by the new mock stream generation "
        "methodology. See {} for information about the new functionality."
        .format(_transition_guide_url))


def streakline_stream(hamiltonian, prog_orbit, prog_mass, release_every=1,
                      Integrator=DOPRI853Integrator, Integrator_kwargs=dict(),
                      snapshot_filename=None, output_every=1, seed=None):
    """This function has been deprecated!

    See {} for more information.

    Parameters
    ----------
    hamiltonian : `~gala.potential.Hamiltonian`
        The system Hamiltonian.
    prog_orbit : `~gala.dynamics.Orbit`
            The orbit of the progenitor system.
    prog_mass : numeric, array_like
        A single mass or an array of masses if the progenitor mass evolves
        with time.
    release_every : int (optional)
        Release particles at the Lagrange points every X timesteps.
    Integrator : `~gala.integrate.Integrator` (optional)
        Integrator to use.
    Integrator_kwargs : dict (optional)
        Any extra keyword argumets to pass to the integrator function.
    snapshot_filename : str (optional)
        Filename to save all incremental snapshots of particle positions and
        velocities. Warning: this can make very large files if you are not
        careful!
    output_every : int (optional)
        If outputing snapshots (i.e., if snapshot_filename is specified), this
        controls how often to output a snapshot.
    seed : int (optional)
        A random number seed for initializing the particle positions.

    Returns
    -------
    stream : `~gala.dynamics.PhaseSpacePosition`

    """
    warnings.warn("This function is deprecated - use the new mock stream "
                  "generation functionality. See {} for more information."
                  .format(_transition_guide_url), DeprecationWarning)

    if Integrator is not DOPRI853Integrator:
        raise ValueError("Integrator must be DOPRI853Integrator.")

    rnd = np.random.RandomState(seed)
    df = StreaklineStreamDF(random_state=rnd)

    gen = MockStreamGenerator(df=df, hamiltonian=hamiltonian)
    stream, _ = gen.run(prog_orbit[0], prog_mass=prog_mass,
                        release_every=release_every, t=prog_orbit.t)

    return stream


def fardal_stream(hamiltonian, prog_orbit, prog_mass, release_every=1,
                  Integrator=DOPRI853Integrator, Integrator_kwargs=dict(),
                  snapshot_filename=None, seed=None, output_every=1):
    """This function has been deprecated!

    See {} for more information.

    Parameters
    ----------
    hamiltonian : `~gala.potential.Hamiltonian`
            The system Hamiltonian.
    prog_orbit : `~gala.dynamics.Orbit`
            The orbit of the progenitor system.
    prog_mass : numeric, array_like
        A single mass or an array of masses if the progenitor mass evolves
        with time.
    release_every : int (optional)
        Release particles at the Lagrange points every X timesteps.
    Integrator : `~gala.integrate.Integrator` (optional)
        Integrator to use.
    Integrator_kwargs : dict (optional)
        Any extra keyword argumets to pass to the integrator function.
    snapshot_filename : str (optional)
        Filename to save all incremental snapshots of particle positions and
        velocities. Warning: this can make very large files if you are not
        careful!
    output_every : int (optional)
        If outputing snapshots (i.e., if snapshot_filename is specified), this
        controls how often to output a snapshot.
    seed : int (optional)
        A random number seed for initializing the particle positions.

    Returns
    -------
    stream : `~gala.dynamics.PhaseSpacePosition`

    """
    warnings.warn("This function is deprecated - use the new mock stream "
                  "generation functionality. See {} for more information."
                  .format(_transition_guide_url), DeprecationWarning)

    if Integrator is not DOPRI853Integrator:
        raise ValueError("Integrator must be DOPRI853Integrator.")

    rnd = np.random.RandomState(seed)
    df = FardalStreamDF(random_state=rnd)

    gen = MockStreamGenerator(df=df, hamiltonian=hamiltonian)
    stream, _ = gen.run(prog_orbit[0], prog_mass=prog_mass,
                        release_every=release_every, t=prog_orbit.t)

    return stream


def dissolved_fardal_stream(hamiltonian, prog_orbit, prog_mass, t_disrupt, release_every=1,
                            Integrator=DOPRI853Integrator, Integrator_kwargs=dict(),
                            snapshot_filename=None, output_every=1, seed=None):
    """DEPRECATED!"""
    raise NotImplementedError(
        "This function has been deprecated by the new mock stream generation "
        "methodology. See {} for information about the new functionality."
        .format(_transition_guide_url))


streakline_stream.__doc__ = streakline_stream.__doc__.format(_transition_guide_url)
fardal_stream.__doc__ = fardal_stream.__doc__.format(_transition_guide_url)
