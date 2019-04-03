#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:46:58 2019

@author: parisarezaie
"""

def plot(data, data_normalized, window_size):

    colors = [ 'green','red']

    for item in iot_m:

        fig, (ax1, ax2,ax3) = plt.subplots(3, 1, figsize=(10, 5))
        t1 = data.index.values
        ax1.scatter(t1, data[item], c=data['TrueOK'].apply(
            lambda x: colors[x]), label='Data')
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Feature Value')
        ax1.tick_params('y')
        ax1.plot(t1, df_rolling_median[item], c='yellow', label='RM')
        ax1.plot(
            t1, df_rolling_median[item]+df_rolling_std[item], c='black', label='RSD')
        ax1.plot(
            t1, df_rolling_median[item]-df_rolling_std[item], c='black', label='RSD')
        ax1.legend(loc="upper right")

        ax2.scatter(t1, data_normalized[item],
                   c=data_normalized['TrueOK'].apply(
            lambda x: colors[x]), label='Normalized Data')
        ax2.set_ylabel('Feature Value')
        ax2.set_xlabel('Index')
        ax2.tick_params('y')
        ax2.legend(loc="upper right")
        
        
        for (group, df), c in zip(data_normalized.groupby('TrueOK'), colors):
            mu=df.loc[:, item].mean(axis=0)
            sigma=df.loc[:, item].std(axis=0)
            den=np.sqrt(df.shape[0])
            sig_den=sigma/den
            mu_e, sigma_e = norm.fit(df.loc[:, item])
            mu_e=float("%0.2f"%mu_e)
            sigma_e=float("%0.2f"%sigma_e)


            
            custome_label=f"""$\mu = {mu:.3f}\pm {sig_den:.3f}$
$\sigma = {sigma:.3f} \pm {sig_den:.3f}$"""
            
            if group==0:
                
                n_equal_bins = 30  
                ax3.hist(df.loc[:, item], histtype="stepfilled", alpha=.8,color=c,label='',density=1,bins=n_equal_bins)
            
                first_edge, last_edge = df.loc[:, item].min(),  df.loc[:, item].max()

                bin_edges = np.linspace(start=first_edge, stop=last_edge,
                         num=n_equal_bins + 1, endpoint=True)

            if group==1:
                ax3.hist(df.loc[:, item], histtype="stepfilled", alpha=.4,color=c,label='',density=1,bins=bin_edges)    
            
            if group==0:

                x = np.linspace(first_edge, last_edge, 100)
                p = norm.pdf(x, mu_e, sigma_e)
                ax3.plot(x, p, 'k', linewidth=2,color=c,label=custome_label)
            
        
        
        ax3.legend(loc="upper right")
        ax3.set_xlabel(
            'Parameter: {0}; WindowSize: {1}'.format(item, window_size))
        fig.tight_layout()
        plt.show()
       
        fig.savefig(os.path.join("Plots",'Figure {0}; WindowSize= {1}.pdf'.format(item,window_size)),dpi=300)
        fig.savefig(os.path.join("Plots",'Figure {0}; WindowSize= {1}.png'.format(item,window_size)),dpi=300)
        


        print('      =======================================================================================')