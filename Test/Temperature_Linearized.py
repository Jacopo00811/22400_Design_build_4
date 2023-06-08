from machine import Pin
from machine import ADC
from machine import DAC
from math import log

import machine
import utime

adc_V_lookup = [0.03705883, 0.02882353, 0.05764706, 0.08647059, 0.08955883, 0.09264707, 0.0957353, 0.09882354, 0.1029412, 0.1070588, 0.1111765, 0.1142647, 0.117353, 0.1204412, 0.1235294, 0.1276471, 0.1317647, 0.1358824, 0.1389706, 0.1420588, 0.1451471, 0.1482353, 0.1523529, 0.1564706, 0.1605882, 0.1636765, 0.1667647, 0.1698529, 0.1729412, 0.1760294, 0.1791177, 0.1822059, 0.1852941, 0.1883824, 0.1914706, 0.1945588, 0.1976471, 0.2007353, 0.2038235, 0.2069118, 0.21, 0.2130883, 0.2161765, 0.2192647, 0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2377941, 0.2408824, 0.2439706, 0.2470588, 0.2501471, 0.2532353, 0.2563236, 0.2594118, 0.2635294, 0.2676471, 0.2717647, 0.274853, 0.2779412, 0.2810294, 0.2841177, 0.2872059, 0.2902942, 0.2933824, 0.2964706, 0.3005883, 0.3047059, 0.3088235, 0.3119118, 0.315, 0.3180882, 0.3211765, 0.3252941, 0.3294118, 0.3335294, 0.3366177, 0.3397059, 0.3427941, 0.3458824, 0.3489706, 0.3520588, 0.3551471, 0.3582353, 0.362353, 0.3664706, 0.3705883, 0.3736765, 0.3767647, 0.379853, 0.3829412, 0.3860294, 0.3891177, 0.3922059, 0.3952941, 0.3994118, 0.4035295, 0.4076471, 0.4107353, 0.4138236, 0.4169118, 0.42, 0.4230883, 0.4261765, 0.4292647, 0.432353, 0.4385294, 0.4447059, 0.4477942, 0.4508824, 0.4539706, 0.4570589, 0.4601471, 0.4632353, 0.4663236, 0.4694118, 0.4725, 0.4755883, 0.4786765, 0.4817647, 0.4858823, 0.4900001, 0.4941177, 0.4965883, 0.4990589, 0.5015294, 0.504, 0.5064706, 0.5095589, 0.5126471, 0.5157353, 0.5188236, 0.5229412, 0.5270588, 0.5311765, 0.5342648, 0.537353, 0.5404412, 0.5435295, 0.5466177, 0.5497059, 0.5527942, 0.5558824, 0.56, 0.5641177, 0.5682353, 0.5713236, 0.5744118, 0.5775001, 0.5805883, 0.5836765, 0.5867648, 0.589853, 0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6094118, 0.6135294, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6330882, 0.6361765, 0.6392647, 0.642353, 0.6464706, 0.6505883, 0.6547059, 0.6577941, 0.6608824, 0.6639706, 0.6670588, 0.670147, 0.6732353, 0.6763235, 0.6794118, 0.6825, 0.6855883, 0.6886765, 0.6917647, 0.6958824, 0.7, 0.7041177, 0.7082353, 0.712353, 0.7164706, 0.7189412, 0.7214118, 0.7238824, 0.7263529, 0.7288236, 0.7329412, 0.7370589, 0.7411765, 0.7442647, 0.747353, 0.7504412, 0.7535295, 0.757647, 0.7617648, 0.7658824, 0.7689706, 0.7720589, 0.7751471, 0.7782353, 0.7823529, 0.7864707, 0.7905883, 0.7947059, 0.7988235, 0.8029412, 0.8060294, 0.8091177, 0.8122059, 0.8152942, 0.8194118, 0.8235294, 0.8276471, 0.8307353, 0.8338236, 0.8369118, 0.8400001, 0.8430882, 0.8461765, 0.8492647, 0.852353, 0.8564707, 0.8605883, 0.8647059, 0.8677941, 0.8708824, 0.8739706, 0.8770589, 0.8801471, 0.8832354, 0.8863235, 0.8894118, 0.8925, 0.8955883, 0.8986765, 0.9017648, 0.9058825, 0.91, 0.9141177, 0.9172059, 0.9202942, 0.9233824, 0.9264707, 0.9295588, 0.9326471, 0.9357353, 0.9388236, 0.9419118, 0.9450001, 0.9480883, 0.9511765, 0.9542647, 0.957353, 0.9604412, 0.9635295, 0.9666177, 0.969706, 0.9727942, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9923531, 0.9964705, 1.000588, 1.003059, 1.005529, 1.008, 1.010471, 1.012941, 1.017059, 1.021176, 1.025294, 1.028382, 1.031471, 1.034559, 1.037647, 1.040735, 1.043824, 1.046912, 1.05, 1.053088, 1.056177, 1.059265, 1.062353, 1.065441, 1.068529, 1.071618, 1.074706, 1.078824, 1.082941, 1.087059, 1.091177, 1.095294, 1.099412, 1.1025, 1.105588, 1.108677, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.127206, 1.130294, 1.133382, 1.136471, 1.140588, 1.144706, 1.148824, 1.151912, 1.155, 1.158088, 1.161177, 1.164265, 1.167353, 1.170441, 1.17353, 1.176, 1.178471, 1.180941, 1.183412, 1.185882, 1.198235, 1.200706, 1.203176, 1.205647, 1.208118, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.229118, 1.235294, 1.237765, 1.240235, 1.242706, 1.245177, 1.247647, 1.250735, 1.253824, 1.256912, 1.26, 1.264118, 1.268235, 1.272353, 1.275441, 1.278529, 1.281618, 1.284706, 1.287794, 1.290882, 1.293971, 1.297059, 1.301177, 1.305294, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.324853, 1.327941, 1.331029, 1.334118, 1.337206, 1.340294, 1.343382, 1.346471, 1.349559, 1.352647, 1.355735, 1.358824, 1.361912, 1.365, 1.368088, 1.371176, 1.374265, 1.377353, 1.380441, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.398971, 1.402059, 1.405147, 1.408235, 1.411324, 1.414412, 1.4175, 1.420588, 1.426765, 1.432941, 1.435412, 1.437882, 1.440353, 1.442824, 1.445294, 1.449412, 1.453529, 1.457647, 1.460118, 1.462588, 1.465059, 1.46753, 1.47, 1.476177, 1.482353, 1.484824, 1.487294, 1.489765, 1.492235, 1.494706, 1.500882, 1.507059, 1.509529, 1.512, 1.514471, 1.516941, 1.519412, 1.52353, 1.527647, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.547206, 1.550294, 1.553382, 1.556471, 1.560588, 1.564706, 1.568824, 1.572941, 1.577059, 1.581177, 1.587353, 1.593529, 1.596, 1.598471, 1.600941, 1.603412, 1.605882, 1.608971, 1.612059, 1.615147, 1.618235, 1.630588, 1.633059, 1.635529, 1.638, 1.640471, 1.642941, 1.646029, 1.649118, 1.652206, 1.655294, 1.658382, 1.661471, 1.664559, 1.667647, 1.673824, 1.68, 1.682059, 1.684118, 1.686177, 1.688235, 1.690294, 1.692353, 1.698529, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.721177, 1.725294, 1.729412, 1.731882, 1.734353, 1.736824, 1.739294, 1.741765, 1.745882, 1.75, 1.754118, 1.757206, 1.760294, 1.763382, 1.766471, 1.770588, 1.774706, 1.778824, 1.781912, 1.785, 1.788088, 1.791177, 1.793647, 1.796118, 1.798588, 1.801059, 1.80353, 1.806, 1.808471, 1.810941, 1.813412, 1.815882, 1.82, 1.824118, 1.828235, 1.834412, 1.840588, 1.843059, 1.845529, 1.848, 1.850471, 1.852941, 1.85603, 1.859118, 1.862206, 1.865294, 1.868382, 1.871471, 1.874559, 1.877647, 1.881765, 1.885882, 1.89, 1.893088, 1.896177, 1.899265, 1.902353, 1.908529, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059, 1.930147, 1.933235, 1.936324, 1.939412, 1.9425, 1.945588, 1.948677, 1.951765, 1.954853, 1.957941, 1.96103, 1.964118, 1.968235, 1.972353, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.991912, 1.995, 1.998088, 2.001177, 2.004265, 2.007353, 2.010441, 2.01353, 2.019706, 2.025882, 2.028353, 2.030823, 2.033294, 2.035765, 2.038235, 2.042353, 2.046471, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.06603, 2.069118, 2.072206, 2.075294, 2.079412, 2.083529, 2.087647, 2.091765, 2.095882, 2.1, 2.103088, 2.106177, 2.109265, 2.112353, 2.115441, 2.11853, 2.121618, 2.124706, 2.127794, 2.130883, 2.133971, 2.137059, 2.141176, 2.145294, 2.149412, 2.1525, 2.155588, 2.158677, 2.161765, 2.164235, 2.166706, 2.169177, 2.171647, 2.174118, 2.178235, 2.182353, 2.186471, 2.189559, 2.192647, 2.195735, 2.198824, 2.202941, 2.207059, 2.211177, 2.213647, 2.216118, 2.218588, 2.221059, 2.22353, 2.226618, 2.229706, 2.232794, 2.235883, 2.238971, 2.242059, 2.245147, 2.248235, 2.252353, 2.256471, 2.260588, 2.263677, 2.266765, 2.269853, 2.272941, 2.277059, 2.281177, 2.285294, 2.287765, 2.290235, 2.292706, 2.295177, 2.297647, 2.301765, 2.305882, 2.31, 2.313088, 2.316177, 2.319265, 2.322353, 2.325441, 2.32853, 2.331618, 2.334706, 2.337794, 2.340883, 2.343971, 2.347059, 2.350147, 2.353235, 2.356324, 2.359412, 2.371765, 2.374853, 2.377941, 2.381029, 2.384118, 2.387206, 2.390294, 2.393382, 2.396471, 2.398941, 2.401412, 2.403883, 2.406353, 2.408823, 2.412941, 2.417059, 2.421176, 2.423647, 2.426118, 2.428588, 2.431059, 2.433529, 2.437647, 2.441765, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.461323, 2.464412, 2.4675, 2.470588, 2.473676, 2.476765, 2.479853, 2.482941, 2.486029, 2.489118, 2.492206, 2.495294, 2.498382, 2.501471, 2.504559, 2.507647, 2.511765, 2.515882, 2.52, 2.522471, 2.524941, 2.527412, 2.529882, 2.532353, 2.536471, 2.540588, 2.544706, 2.546765, 2.548824, 2.550882, 2.552941, 2.555, 2.557059, 2.560147, 2.563235, 2.566324, 2.569412, 2.571882, 2.574353, 2.576824, 2.579294, 2.581765, 2.585882, 2.59, 2.594118, 2.596588, 2.599059, 2.60153, 2.604, 2.606471, 2.609559, 2.612647, 2.615735, 2.618824, 2.621294, 2.623765, 2.626235, 2.628706, 2.631176, 2.633235, 2.635294, 2.637353, 2.639412, 2.641471, 2.643529, 2.646618, 2.649706, 2.652794, 2.655882, 2.66, 2.664118, 2.668235, 2.670294, 2.672353, 2.674412, 2.676471, 2.67853, 2.680588, 2.682647, 2.684706, 2.686765, 2.688824, 2.690882, 2.692941, 2.697059, 2.701177, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720735, 2.723824, 2.726912, 2.73, 2.732059, 2.734118, 2.736176, 2.738235, 2.740294, 2.742353, 2.744824, 2.747294, 2.749765, 2.752235, 2.754706, 2.757176, 2.759647, 2.762118, 2.764588, 2.767059, 2.769118, 2.771177, 2.773235, 2.775294, 2.777353, 2.779412, 2.7825, 2.785588, 2.788677, 2.791765, 2.793824, 2.795882, 2.797941, 2.8, 2.802059, 2.804118, 2.806588, 2.809059, 2.81153, 2.814, 2.816471, 2.818941, 2.821412, 2.823883, 2.826353, 2.828824, 2.830588, 2.832353, 2.834118, 2.835882, 2.837647, 2.839412, 2.841177, 2.844265, 2.847353, 2.850441, 2.853529, 2.855588, 2.857647, 2.859706, 2.861765, 2.863824, 2.865882, 2.867941, 2.87, 2.872059, 2.874118, 2.876177, 2.878235, 2.880294, 2.882353, 2.884412, 2.886471, 2.88853, 2.890588, 2.893677, 2.896765, 2.899853, 2.902941, 2.904486, 2.90603, 2.907574, 2.909118, 2.910662, 2.912206, 2.91375, 2.915294, 2.916838, 2.918382, 2.919927, 2.921471, 2.923015, 2.924559, 2.926103, 2.927647, 2.930118, 2.932588, 2.935059, 2.93753, 2.94, 2.942059, 2.944118, 2.946177, 2.948236, 2.950294, 2.952353, 2.953897, 2.955441, 2.956985, 2.958529, 2.960074, 2.961618, 2.963162, 2.964706, 2.966471, 2.968235, 2.97, 2.971765, 2.973529, 2.975294, 2.977059, 2.979118, 2.981177, 2.983235, 2.985294, 2.987353, 2.989412, 2.991471, 2.99353, 2.995588, 2.997647, 2.999706, 3.001765, 3.00353, 3.005294, 3.007059, 3.008824, 3.010588, 3.012353, 3.014118, 3.016588, 3.019059, 3.02153, 3.024, 3.026471, 3.028015, 3.029559, 3.031103, 3.032647, 3.034191, 3.035735, 3.03728, 3.038824, 3.040883, 3.042941, 3.045, 3.047059, 3.049118, 3.051177, 3.052721, 3.054265, 3.055809, 3.057353, 3.058897, 3.060441, 3.061985, 3.063529, 3.065588, 3.067647, 3.069706, 3.071765, 3.073823, 3.075882, 3.077427, 3.078971, 3.080515, 3.082059, 3.083603, 3.085147, 3.086691, 3.088235, 3.09, 3.091765, 3.093529, 3.095294, 3.097059, 3.098824, 3.100588, 3.102647, 3.104706, 3.106765, 3.108824, 3.110882, 3.112941, 3.114314, 3.115686, 3.117059, 3.118431, 3.119804, 3.121177, 3.122549, 3.123922, 3.125294, 3.127059, 3.128824, 3.130588, 3.132353, 3.134118, 3.135883, 3.137647, 3.139706, 3.141765, 3.143824, 3.145883, 3.147941, 3.15, 3.15, 3.15]

NOM_RES = 10000
SER_RES = 9820
TEMP_NOM = 25
NUM_SAMPLES = 25
THERM_B_COEFF = 3950
ADC_MAX = 1023
ADC_Vmax = 3.15

class TempSensor:
    def __init__(self, pinNoTemp = 32)-> None:
        """
            Temperature Sensor constructor with default pin no. 32.

            Params:
                pinNoTemp - number of the pin in which the sensor is connected
        """
        self.adc = ADC(Pin(pinNoTemp))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)
        
    # Time ticks 13000 Microseconds
    def read_temp(self):
        """
            Method to measure the temperature from the thermistor.
            The returned result is averaged over 25 measurements.
        """
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, NUM_SAMPLES+1):
            raw_read.append(self.adc.read())

        # Average of the NUM_SAMPLES and look it up in the table after linearization
        raw_average = sum(raw_read)/NUM_SAMPLES
        #print('raw_avg = ' + str(raw_average))
        #print('V_measured = ' + str(adc_V_lookup[round(raw_average)]))

        # Convert the voltage to resistance
        raw_average = ADC_MAX * adc_V_lookup[round(raw_average)]/ADC_Vmax
        # print(raw_average)
        # print(len(adc_V_lookup))
        resistance = (SER_RES * raw_average) / (ADC_MAX - raw_average)
        # print('Thermistor resistance: {} ohms'.format(resistance))

        # Convert resistance to temperature
        steinhart  = -log(resistance / NOM_RES) / THERM_B_COEFF
        steinhart += 1.0 / (TEMP_NOM + 273.15)
        steinhart  = (1.0 / steinhart) - 273.15
        print('Temperature: {}°C'.format(steinhart))
        return steinhart

# def init_temp_sensor(TENP_SENS_ADC_PIN_NO = 32):
#     adc = ADC(Pin(TENP_SENS_ADC_PIN_NO))
#     adc.atten(ADC.ATTN_11DB)
#     adc.width(ADC.WIDTH_10BIT)
#     return adc

# def read_temp(temp_sens):
#     raw_read = []
#     # Collect NUM_SAMPLES
#     for i in range(1, NUM_SAMPLES+1):
#         raw_read.append(temp_sens.read())

#     # Average of the NUM_SAMPLES and look it up in the table
#     raw_average = sum(raw_read)/NUM_SAMPLES
#     print('raw_avg = ' + str(raw_average))
#     print('V_measured = ' + str(adc_V_lookup[round(raw_average)]))

#     # Convert to resistance
#     raw_average = ADC_MAX * adc_V_lookup[round(raw_average)]/ADC_Vmax
#     resistance = (SER_RES * raw_average) / (ADC_MAX - raw_average)
#     print('Thermistor resistance: {} ohms'.format(resistance))

#     # Convert to temperature
#     steinhart  = log(resistance / NOM_RES) / THERM_B_COEFF
#     steinhart += 1.0 / (TEMP_NOM + 273.15)
#     steinhart  = (1.0 / steinhart) - 273.15
#     return steinhart

print("I'm alive!\n")
utime.sleep_ms(2000)

temp_sens = TempSensor()

sample_last_ms = 0
SAMPLE_INTERVAL = 1000

while (True):
    if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= SAMPLE_INTERVAL:
        temp = temp_sens.read_temp(temp_sens)
        print('Thermistor temperature: ' + str(temp))
        sample_last_ms = utime.ticks_ms()
