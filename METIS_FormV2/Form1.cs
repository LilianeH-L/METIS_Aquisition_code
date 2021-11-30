using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;

namespace METIS_FormV2
{
    public partial class Form1 : Form
    {
        #region Variables
        string lineDataIn;
        byte[] commandToSend = { 2 };
        int index, serialDataIn, indexOfStop;
        int[] dataArray = new int[200];

        #endregion


        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            btnOpenPort.Enabled = true;
            btnStart.Enabled = false;
            btnStop.Enabled = false;
            cbBaudRate.Text = "9600";

            chartDataM1.Series["Data"].Points.AddXY(1, 1);
            chartDataM1.ChartAreas[0].AxisX.Maximum = 200;
            chartDataM1.ChartAreas[0].AxisX.Minimum = 0;
            chartDataM1.ChartAreas[0].AxisY.Maximum = 4096;
            chartDataM1.ChartAreas[0].AxisY.Minimum = 0;
        }

        #region Buttons
        private void btnOpenPort_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort1.PortName = cbComPorts.Text;
                serialPort1.BaudRate = Convert.ToInt32(cbBaudRate.Text);

                btnOpenPort.Enabled = false;
                btnStart.Enabled = true;
                btnStop.Enabled = false;

                chartDataM1.Series["Data"].Points.Clear();

            }
            catch(Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen == false)
            {
                serialPort1.Open();
            }

            btnStart.Enabled = false;
            btnStop.Enabled = true;
            cbComPorts.Enabled = false;
            cbBaudRate.Enabled = false;

            commandToSend[0] = 1;
            serialPort1.Write(commandToSend, 0, 1);
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            try
            {
                btnStart.Enabled = true;
                btnStop.Enabled = false;

                commandToSend[0] = 2;
                serialPort1.Write(commandToSend, 0, 1);
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }
        #endregion

        #region ComboBox
        private void cbComPorts_DropDown(object sender, EventArgs e)
        {
            string[] portsList = SerialPort.GetPortNames();
            cbComPorts.Items.Clear();
            cbComPorts.Items.AddRange(portsList);
        }
        #endregion



        #region Data Reception
        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            //Read line printed by Teensy after converting a value
            lineDataIn = serialPort1.ReadLine();

            //Process line
            indexOfStop = lineDataIn.IndexOf('%');
            serialDataIn = Convert.ToInt32(lineDataIn.Substring(0, indexOfStop));

            this.BeginInvoke(new EventHandler(UpdateArray));
        }

        private void UpdateArray(object sender, EventArgs e)
        {
            try
            {
                if (index < 1)
                {
                    chartDataM1.Series["Data"].Points.AddY(serialDataIn);
                    chartDataM1.Series["Data"].Points.Clear();
                    index++;
                }
                else
                {
                    ShiftData(dataArray, serialDataIn);
                    chartDataM1.Series["Data"].Points.Clear();
                    for (int i = 0; i < dataArray.Length - 1; i++)
                    {
                        chartDataM1.Series["Data"].Points.AddY(dataArray[i]);
                    }
                }
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }

        private void ShiftData(int[] array, int newValue)
        {
            for (int i = 1; i < array.Length; i++)
            {
                array[i - 1] = array[i];
                array[array.Length - 1] = newValue;
            }
        }

        #endregion
    }
}
