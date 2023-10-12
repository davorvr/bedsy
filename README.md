# BeDSy - Behaviour-recording Device Synchroniser

#### What is it?

The **BeDSy (Behaviour-recording Device Synchroniser)** is a platform for hardware triggering and synchronisation of equipment for laboratory animal behavioural monitoring.

It consists of two components: this Python package, which interfaces with the **[BeDsyino](https://github.com/davorvr/bedsyino)**, a hardware platform which sends custom trigger signals to animal behaviour-monitoring devices.

#### How to install?

BeDSy is [available on PyPi](https://pypi.org/project/bedsy/) can be installed with `pip`:

```bash
pip install bedsy
```

##### Dependencies

 * [pySerial](https://pypi.org/project/pyserial/) - can be also be installed with `pip`

#### History

I (Davor Virag) developed the BeDSy platform with immense help from Paul Mieske and indispensible advice by Pia Kahnau during my stay with them at the [German Federal Institute for Risk Assessment (BfR)](https://www.bfr.bund.de/) in September 2023, where I was gracefully hosted by their brilliant PI, Lars Lewejohann, as part of my Short-Term Scientific Mission (STSM) funded by the [COST](https://cost.eu/) action ["Improving biomedical research by automated behaviour monitoring in the animal home-cage - TEATIME" (CA20135)](https://cost-teatime.org/).

BeDSy was originally developed to improve video and audio synchronisation between several Basler cameras and the AviSoft UltraSoundGate for Paul's very cool upcoming research project.

#### Current state

This package is quite simple and seems to work fairly well. I don't have any major plans for it, except for adding sorely needed comments and documentation. It's currently been tested on Windows only, but I think it should work on Linux as well.

For an example (though not very clean) implementation into an existing project, see [Basler GUI Updated](https://github.com/RefinementReferenceCenter/basler_gui_updated), a continuation of Niek Andresen's [Basler GUI Py](https://github.com/RefinementReferenceCenter/basler_gui_py) project.

The [BeDsyino](https://github.com/davorvr/bedsyino) is, however, still cooking. While the code is mostly complete, only a single hand-soldered, protoboard-based prototype has been developed thus far. A modular, extensible hardware platform is currently in the works. For more info, please check that repo.

#### How does it work

The module provides communication with [BeDsyino](https://github.com/davorvr/bedsyino), but requires the user to handle start/stop messages (i.e. it won't raise an exception if it doesn't receive a stop message after calling the `stop_bedsy()` method).

*TO DO - expand*

#### License

The code is distributed under GPLv3.
