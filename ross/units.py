"""This module deals with units conversion in the ROSS library."""

import inspect
import json
import time
import warnings
from functools import wraps
from pathlib import Path

import pint

new_units_path = Path(__file__).parent / "new_units.txt"
ureg = pint.get_application_registry()
if isinstance(ureg.get(), pint.registry.LazyRegistry):
    ureg = pint.UnitRegistry()
    ureg.load_definitions(str(new_units_path))
    # set ureg to make pickle possible
    pint.set_application_registry(ureg)

Q_ = ureg.Quantity
_DEBUG_LOG_PATH = Path("/home/cristofer/GitHub/ross/.cursor/debug-75e502.log")
_DEBUG_SESSION_ID = "75e502"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pint.Quantity([])

__all__ = ["Q_", "check_units"]


def _debug_log(hypothesis_id, location, message, data):
    payload = {
        "sessionId": _DEBUG_SESSION_ID,
        "runId": "pre-fix",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")
    except Exception:
        pass


def _convert_sequence_with_units(value, unit_name):
    if not isinstance(value, (list, tuple)):
        return None
    converted = []
    for item in value:
        try:
            converted.append(item.to(unit_name).m)
        except AttributeError:
            converted.append(Q_(item, unit_name).m)
    return converted if isinstance(value, list) else tuple(converted)

units = {
    "E": "N/m**2",
    "G_s": "N/m**2",
    "rho": "kg/m**3",
    "density": "kg/m**3",
    "L": "meter",
    "idl": "meter",
    "idr": "meter",
    "odl": "meter",
    "odr": "meter",
    "id": "meter",
    "od": "meter",
    "i_d": "meter",
    "o_d": "meter",
    "speed": "radian/second",
    "frequency": "radian/second",
    "m": "kg",
    "mx": "kg",
    "my": "kg",
    "Ip": "kg*m**2",
    "Id": "kg*m**2",
    "width": "meter",
    "depth": "meter",
    "thickness": "meter",
    "pitch": "meter",
    "height": "meter",
    "radius": "meter",
    "diameter": "meter",
    "clearance": "meter",
    "length": "meter",
    "distance": "meter",
    "area": "meter**2",
    "unbalance_magnitude": "kg*m",
    "unbalance_phase": "rad",
    "pressure": "pascal",
    "pressure_ratio": "dimensionless",
    "p": "pascal",
    "temperature": "degK",
    "T": "degK",
    "velocity": "m/s",
    "angle": "rad",
    "arc": "rad",
    "convection": "W/(m²*degK)",
    "conductivity": "W/(m*degK)",
    "expansion": "1/degK",
    "stiffness": "N/m",
    "damping": "N*s/m",
    "weight": "N",
    "load": "N",
    "force": "N",
    "torque": "N*m",
    "flow_v": "meter**3/second",
    "flow_m": "kilogram/second",
    "fit": "m",
    "viscosity": "pascal*s",
    "h": "joule/kilogram",
    "s": "joule/(kelvin kilogram)",
    "b": "meter",
    "D": "meter",
    "d": "meter",
    "roughness": "meter",
    "head": "joule/kilogram",
    "eff": "dimensionless",
    "power": "watt",
    "module": "meter",
}
for i, unit in zip(["k", "c", "m"], ["N/m", "N*s/m", "kg"]):
    for j in ["x", "y", "z"]:
        for k in ["x", "y", "z"]:
            units["".join([i, j, k])] = unit


def check_units(func):
    """Wrapper to check and convert units to base_units.

    If we use the check_units decorator in a function the arguments are checked,
    and if they are in the dictionary, they are converted to the 'default' unit given
    in the dictionary.
    The check is carried out by splitting the argument name on '_', and checking
    if any of the names are in the dictionary. So an argument such as 'inlet_pressure',
    will be split into ['inlet', 'pressure'], and since we have the name 'pressure'
    in the dictionary mapped to 'Pa', we will automatically convert the value to
    this default unit.

    For example:
    >>> units = {
    ... "L": "meter",
    ... }

    >>> @check_units
    ... def foo(L=None):
    ...     print(L)
    ...

    If we call the function with the argument as a float:
    >>> foo(L=0.5)
    0.5

    If we call the function with a pint.Quantity object the value is automatically
    converted to the default:
    >>> foo(L=Q_(0.5, 'inches'))
    0.0127
    """

    @wraps(func)
    def inner(*args, **kwargs):
        base_unit_args = []
        args_names = inspect.getfullargspec(func)[0]
        if func.__name__ == "run_crack":
            # region agent log
            _debug_log(
                "H1",
                "ross/units.py:inner-entry",
                "run_crack entered check_units",
                {
                    "arg_names": args_names,
                    "kwargs_keys": list(kwargs.keys()),
                    "kwargs_types": {k: type(v).__name__ for k, v in kwargs.items()},
                },
            )
            # endregion

        for arg_name, arg_value in zip(args_names, args):
            names = arg_name.split("_")
            if "units" in names:
                base_unit_args.append(arg_value)
                continue

            # treat flow_v and flow_m separately
            if "flow_v" in arg_name:
                names.insert(0, "flow_v")
            if "flow_m" in arg_name:
                names.insert(0, "flow_m")

            if arg_name not in names:
                # check first for arg_name in units
                names.insert(0, arg_name)
            for name in names:
                if name in units and arg_value is not None:
                    # For now, we only return the magnitude for the converted Quantity
                    # If pint is fully adopted by ross in the future, and we have all Quantities
                    # using it, we could remove this, which would allows us to use pint in its full capability
                    try:
                        base_unit_args.append(arg_value.to(units[name]).m)
                    except AttributeError:
                        try:
                            base_unit_args.append(Q_(arg_value, units[name]).m)
                        except TypeError:
                            # Handle erros that we get with bool for example
                            base_unit_args.append(arg_value)
                        except ValueError:
                            seq_value = _convert_sequence_with_units(
                                arg_value, units[name]
                            )
                            if seq_value is not None:
                                # region agent log
                                _debug_log(
                                    "H5",
                                    "ross/units.py:arg-sequence-convert",
                                    "converted positional sequence element-wise after Q_ ValueError",
                                    {
                                        "arg_name": arg_name,
                                        "unit_name": name,
                                        "value_type": type(arg_value).__name__,
                                        "value_len": len(arg_value),
                                    },
                                )
                                # endregion
                                base_unit_args.append(seq_value)
                            else:
                                raise
                        except Exception as exc:
                            # region agent log
                            _debug_log(
                                "H4",
                                "ross/units.py:arg-q-convert",
                                "unexpected exception converting positional arg with Q_",
                                {
                                    "arg_name": arg_name,
                                    "unit_name": name,
                                    "value_type": type(arg_value).__name__,
                                    "exception_type": type(exc).__name__,
                                    "exception": str(exc),
                                },
                            )
                            # endregion
                            raise
                    break
            else:
                base_unit_args.append(arg_value)

        base_unit_kwargs = {}
        for k, v in kwargs.items():
            names = k.split("_")
            if "units" in names:
                base_unit_kwargs[k] = v
                continue

            # treat flow_v and flow_m separately
            if "flow_v" in k:
                names.insert(0, "flow_v")
            if "flow_m" in k:
                names.insert(0, "flow_m")

            if k not in names:
                # check first for arg_name in units
                names.insert(0, k)
            for name in names:
                if name in units and v is not None:
                    if func.__name__ == "run_crack" and k in {
                        "node",
                        "unbalance_magnitude",
                        "unbalance_phase",
                        "speed",
                        "t",
                    }:
                        preview = repr(v)
                        # region agent log
                        _debug_log(
                            "H2",
                            "ross/units.py:kwargs-before-convert",
                            "pre-conversion state for run_crack kwarg",
                            {
                                "kwarg": k,
                                "unit_name": name,
                                "value_type": type(v).__name__,
                                "value_len": len(v) if hasattr(v, "__len__") else None,
                                "first_item_type": (
                                    type(v[0]).__name__
                                    if isinstance(v, (list, tuple)) and len(v) > 0
                                    else None
                                ),
                                "preview": preview[:200],
                            },
                        )
                        # endregion
                    try:
                        base_unit_kwargs[k] = v.to(units[name]).m
                    except AttributeError:
                        if func.__name__ == "run_crack":
                            # region agent log
                            _debug_log(
                                "H3",
                                "ross/units.py:kwargs-attrerror",
                                "kwarg has no .to(); falling back to Q_ conversion",
                                {
                                    "kwarg": k,
                                    "unit_name": name,
                                    "value_type": type(v).__name__,
                                },
                            )
                            # endregion
                        try:
                            base_unit_kwargs[k] = Q_(v, units[name]).m
                        except TypeError:
                            # Handle errors that we get with bool for example
                            base_unit_kwargs[k] = v
                        except ValueError:
                            seq_value = _convert_sequence_with_units(v, units[name])
                            if seq_value is not None:
                                # region agent log
                                _debug_log(
                                    "H5",
                                    "ross/units.py:kwargs-sequence-convert",
                                    "converted kwarg sequence element-wise after Q_ ValueError",
                                    {
                                        "kwarg": k,
                                        "unit_name": name,
                                        "value_type": type(v).__name__,
                                        "value_len": len(v),
                                    },
                                )
                                # endregion
                                base_unit_kwargs[k] = seq_value
                            else:
                                raise
                        except Exception as exc:
                            # region agent log
                            _debug_log(
                                "H4",
                                "ross/units.py:kwargs-q-convert",
                                "unexpected exception converting kwarg with Q_",
                                {
                                    "kwarg": k,
                                    "unit_name": name,
                                    "value_type": type(v).__name__,
                                    "exception_type": type(exc).__name__,
                                    "exception": str(exc),
                                },
                            )
                            # endregion
                            raise
                    break
            else:
                base_unit_kwargs[k] = v

        if func.__name__ == "run_crack":
            # region agent log
            _debug_log(
                "H6",
                "ross/units.py:before-func-call",
                "about to call run_crack with converted kwargs",
                {
                    "converted_types": {
                        k: type(v).__name__ for k, v in base_unit_kwargs.items()
                    },
                    "converted_lengths": {
                        k: len(v) if hasattr(v, "__len__") else None
                        for k, v in base_unit_kwargs.items()
                    },
                },
            )
            # endregion
        try:
            result = func(*base_unit_args, **base_unit_kwargs)
            if func.__name__ == "run_crack":
                # region agent log
                _debug_log(
                    "H6",
                    "ross/units.py:after-func-call",
                    "run_crack returned successfully",
                    {"result_type": type(result).__name__},
                )
                # endregion
            return result
        except Exception as exc:
            if func.__name__ == "run_crack":
                # region agent log
                _debug_log(
                    "H7",
                    "ross/units.py:func-exception",
                    "run_crack raised exception after unit conversion",
                    {
                        "exception_type": type(exc).__name__,
                        "exception": str(exc),
                    },
                )
                # endregion
            raise

    return inner
