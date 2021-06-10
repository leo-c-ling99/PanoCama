#include "camera_wrapper.h"

ArduCAM cam1(OV2640, CAMERA_1_CS, Wire, SPI);
ArduCAM cam2(OV2640, CAMERA_2_CS, Wire1, SPI);
//const size_t buffer_size = 4096;

uint8_t image_buffer[buffer_size] = {0xFF};
//SPIClass SPI1(HSPI);

void init_camera(ArduCAM &cam, SPIClass &spi, int cs, TwoWire &i2c)
{
    uint8_t vid, pid;
    uint8_t temp;

    i2c.begin();
    Serial.println("ArduCAM Start!");

    // set the CS as an output:
    pinMode(cs, OUTPUT);

    //Check if the ArduCAM SPI bus is OK
    cam.write_reg(ARDUCHIP_TEST1, 0x55);
    temp = cam.read_reg(ARDUCHIP_TEST1);
    if (temp != 0x55)
    {
        Serial.println("SPI interface Error!");
        while (1);
    }

    //Check if the camera module type is OV2640
    cam.wrSensorReg8_8(0xff, 0x01);
    cam.rdSensorReg8_8(OV2640_CHIPID_HIGH, &vid);
    cam.rdSensorReg8_8(OV2640_CHIPID_LOW, &pid);
    if ((vid != 0x26) && ((pid != 0x41) || (pid != 0x42)))
        Serial.println("Can't find OV2640 module!");
    else
        Serial.println("OV2640 detected.");

    //Change to JPEG capture mode and initialize the OV2640 module
    cam.set_format(JPEG);
    cam.InitCAM();
    cam.OV2640_set_JPEG_size(OV2640_1600x1200);
    cam.clear_fifo_flag();
}

void init_cameras(void)
{
    pinMode(CAMERA_1_CS, OUTPUT);
    pinMode(CAMERA_2_CS, OUTPUT);
    SPI.begin(CAMERA_1_SCK, CAMERA_1_MISO, CAMERA_1_MOSI, CAMERA_1_CS);
    SPI.setFrequency(800000); //8MHz MAX

    //SPI1.begin(CAMERA_2_SCK, CAMERA_2_MISO, CAMERA_2_MOSI, CAMERA_2_CS);
    //SPI1.setFrequency(4000000);

    Wire.begin(CAMERA_1_SDA, CAMERA_1_SCL);
    Wire1.begin(CAMERA_2_SDA, CAMERA_2_SCL);

    init_camera(cam1, SPI, CAMERA_1_CS, Wire);
    init_camera(cam2, SPI, CAMERA_2_CS, Wire1);
}

void start_capture(ArduCAM &cam) {
  cam.clear_fifo_flag();
  cam.start_capture();
}

size_t start_picture_read(ArduCAM &cam)
{
    size_t len = cam.read_fifo_length();
    Serial.println(len);
    if (len >= 0x07ffff)
    {
        Serial.println("Over size.");
        return 0;
    }
    else if (len == 0)
    {
        Serial.println("Size is 0.");
        return 0;
    }

    cam.CS_LOW();
    cam.set_fifo_burst();
#if !(defined(ARDUCAM_SHIELD_V2) && defined(OV2640_CAM))
    SPI.transfer(0xFF);
#endif

    if (len == 0) cam.CS_HIGH();

    return len;
}

size_t fill_picture_buffer(ArduCAM &cam, size_t len)
{
    size_t will_copy = (len < buffer_size) ? len : buffer_size;
    SPI.transferBytes(&image_buffer[0], &image_buffer[0], will_copy);
    len -= will_copy;
    if (len == 0) cam.CS_HIGH();

    return len;
}