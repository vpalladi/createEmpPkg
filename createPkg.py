#!/usr/bin/python3

import argparse 
import os
import shutil
import wget

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-p', action="store", nargs= 1, dest="pkg")
parser.add_argument('-c', action="store", nargs= '*', dest="components")
parser.add_argument('--cp', action="store", nargs= 1, dest="cmpPL")


### gen payload ###
def gen__vhd( dst, name='', is_payload=False ) :
    if is_payload :
        wget.download('https://gitlab.cern.ch:8443/p2-xware/firmware/emp-fwk/blob/master/components/payload/firmware/hdl/emp_payload.vhd')
        shutil.move('emp_payload.vhd', dst)
    else :
        touch = open( dst + '/' + name, 'w' )
        touch.close
        
### .dep ###
def gen__dep( name, component_name='', is_payload=False ) :
    f = open( name+'.dep', 'w')

    file_vhd = os.listdir('../hdl')

    for fi in file_vhd :
        f.write('src '+fi+'\n')

    if is_payload :
        components = os.listdir('../../../')
        print('kkkkkk ',components)

        for comp in components :
            if comp != component_name :
                f.write('src -c '+comp+'\n')
        f.write('src -c emp-fwk:components/datapath emp_data_types.vhd\n')
        f.write('src -c ipbus-firmware:components/ipbus_core ipbus_fabric_sel.vhd ipbus_package.vhd\n') 
        f.write('src -c emp-fwk:components/ttc mp7_ttc_decl.vhd\n')
        f.write('addrtab -t emp_payload.xml\n')


### addr_table ###    
def gen__addr_table_xml( componentName ) :
    f = open(componentName+'.xml', 'w')
    f.write('<node id="'+componentName+'">\n')
    f.write('#<node id="uRAM_0" module="file://uRAM.xml" address="0x0"    fwinfo="endpoint;width=1"/>\n')
    f.write('</node">\n')

def gen__emp_payload_xml() :
    gen__addr_table_xml( 'emp_payload' )

    
### Class component ###
class emp_component :
    
    def __init__( self, name, is_payload=False ) :
        self.name = name
        self.is_payload = is_payload
        
    def generate( self ) :
        
        self.pwd = os.path.abspath( './' )
        self.abs_path = self.pwd+'/'+self.name

        # create (if !exists) component dir and mode there
        print( self.abs_path )
        if not( os.path.exists( self.abs_path ) ) :
            print( 'creating component :'+self.abs_path)
            os.makedirs( self.abs_path )
        else:
            print('path exists')
        os.chdir( self.abs_path )

        # address table
        if not( os.path.exists( 'addr_table' ) ) :
            os.makedirs( 'addr_table' )
            os.chdir( 'addr_table' )            
            if self.is_payload :
                gen__emp_payload_xml()
            else :
                gen__addr_table_xml( self.name )
        os.chdir( self.abs_path )

        # firmware
        if not( os.path.exists( 'firmware' ) ) :
            os.makedirs( 'firmware' )
            os.chdir( 'firmware' )
            
            if not( os.path.exists( 'hdl' ) ) :
                os.makedirs( 'hdl' )
                ### generate an empty .vhd file or a null algo emp_payload.vhd ### 
                gen__vhd( './hdl',
                          name=self.name+'.vhd',
                          is_payload=self.is_payload
                )
            if not( os.path.exists( 'cfg' ) ) :
                os.makedirs( 'cfg' )
                os.chdir( 'cfg' )
                ### generate .dep file ###
                gen__dep( name=self.name,
                          component_name=self.name,
                          is_payload=self.is_payload
                )
                
        os.chdir( self.pwd )
        
                
### Class pkg ###
class emp_pkg :
    def __init__(self, name) :
        self.name = name
        self.components = []

    def add_component(self, name, is_payload=False) :
        if is_payload :
            self.components.append( emp_component( name, is_payload ) )
        else :
            self.components.insert( 0, emp_component( name, is_payload ) )
    def generate(self) :
        if not( os.path.exists( self.name ) ) :
            os.makedirs( self.name )
        os.chdir( self.name )
        for c in self.components :
            c.generate()

def main() :

    args = parser.parse_args()

    print('genereting package:', args.pkg )
    print('genereting componenets:', args.components )


    pkg = emp_pkg( args.pkg[0] )

    for cp in args.cmpPL :
        pkg.add_component( cp, True)

    for cp in args.components :
        pkg.add_component( cp)

    pkg.generate()


main()
print('\n')        
        






