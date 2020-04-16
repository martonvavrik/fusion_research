import flap

def sav_to_flap (loaded_sav, skip_keys = [], create_channel_no=False):
    # loaded_sav: a sav file loaded as a python dictionary, loaded with the io.readsav command
    # skip_keys: which keys to skip when creating coordinate axes
    # and returns a flap.DataObject
    if type(loaded_sav) is not dict:
        raise TypeError('loaded_sav is not a dictionary')

    coordinates=None
    skip_keys.extend["data", "expname", "shotnumber", "data_history", "coord_history"]

    # planned? feature: non-equidistant time axis
    if "timeax" in loaded_sav:
        time_ax = flap.Coordinate(name="Time",
                              unit="s",
                              mode=flap.CoordinateMode(equidistant=True),
                              start=loaded_sav["timeax"][0],
                              step=loaded_sav["timeax"][1] - loaded_sav["timeax"][0],
                              # values=loaded_sav["timeax"]
                              dimension_list=[1]
                              )
        coordinates.append(time_ax)
        skip_keys.append("timeax")

    if "channels" in loaded_sav:
        channel_name = flap.Coordinate(name="Channels",
                                   unit=None,
                                   mode=flap.CoordinateMode(equidistant=False),
                                   values=loaded_sav["channels"],
                                   dimension_list=[0],
                                   shape=len(loaded_sav["channels"])
                                   )
        coordinates.append(channel_name)
        skip_keys.append("channels")

        if create_channel_no:
            channel_no = flap.Coordinate(name="Channel_no",
                                 unit="no",
                                 mode=flap.CoordinateMode(equidistant=True),
                                 start=0,
                                 step=1,
                                 dimension_list=[0]
                                 )
            coordinates.append(channel_no)

    if "theta" in loaded_sav:
        theta_ax = flap.Coordinate(name="Theta",
                               unit="rad",
                               mode=flap.CoordinateMode(equidistant=False),
                               values=loaded_sav["theta"],
                               dimension_list=[0],
                               shape=len(loaded_sav["theta"])
                               )
        coordinates.append(theta_ax)
        skip_keys.append("theta")

    if "phi" in loaded_sav:
        phi_ax = flap.Coordinate(name="Phi",
                             unit="rad",
                             mode=flap.CoordinateMode(equidistant=False),
                             values=loaded_sav["phi"],
                             dimension_list=[0],
                             shape=len(loaded_sav["phi"])
                             )
        coordinates.append(phi_ax)
        skip_keys.append("phi")


    # create coordinate objects for other keys in the dicionary
    for key in loaded_sav:
        if key not in skip_keys:
            try:
                unknown_ax = flap.Coordinate(name=key,
                             unit=None,
                             mode=flap.CoordinateMode(equidistant=False),
                             values=loaded_sav[key],
                             dimension_list=[0],
                             shape=len(loaded_sav[key])
                             )
            except:
                print("Could not generate flap coordinate for " + key + ". You may want to use the skip_keys argument for this key.")


    flap_object = flap.DataObject(
        data_array=loaded_sav['data'],
        data_unit=flap.Unit(name='voltage', unit='volt'),
        exp_id=str(loaded_sav['expname'])[2:-1] + " " + str(loaded_sav['shotnumber']),
        coordinates=coordinates,
        data_shape=loaded_sav['data'].shape
    )

    return flap_object
