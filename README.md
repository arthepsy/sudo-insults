# sudo insults
Reuse [sudo](http://www.sudo.ws) insults.
(_currently only as Python module_)

## generate
Download, parse and generate insults from sudo: 
  ```
  $ python generate_insults.py <insults>

   <insults>  list of insults, separated by comma

   ALL        include all insults
   PC         use politically correct variations

   2001       HAL insults (paraphrased) from 2001
   CLASSIC    Insults from the original sudo
   GOONS      Insults from the Goon Show
   CSOPS      CSOps insults
  ```
Example:
  ```
  $ python generate_insults.py PC,ALL
  ```

## usage
  ```
  $ python demo.py
  Maybe if you used more than just two fingers...
  ```
  ```
  $ python demo.py
  Do you think like you type?
  ```
